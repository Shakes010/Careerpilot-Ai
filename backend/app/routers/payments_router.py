from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header, Request, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
import app.models as models
from app.services.auth_service import get_current_user
from app.config import settings
from app.services.razorpay_service import create_razorpay_order, verify_razorpay_signature, generate_inapp_payment_signature

router = APIRouter(prefix="/payments", tags=["Payments & Subscriptions"])

class CreateOrderRequest(BaseModel):
    plan_id: str

class VerifyPaymentRequest(BaseModel):
    plan_id: str
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    payment_method: Optional[str] = "card"

class ProcessInAppPaymentRequest(BaseModel):
    plan_id: str
    order_id: str
    payment_method: str = "card" # card, upi, netbanking
    card_last4: Optional[str] = None
    upi_vpa: Optional[str] = None
    bank_name: Optional[str] = None

class DirectUpgradeRequest(BaseModel):
    plan_id: str

@router.get("/plans")
def list_subscription_plans(db: Session = Depends(get_db)):
    plans = db.query(models.Plan).order_by(models.Plan.price_inr.asc()).all()
    return [
        {
            "id": str(p.id),
            "plan_name": p.plan_name,
            "tier": p.tier.value,
            "monthly_credits": p.monthly_credits,
            "price_inr": float(p.price_inr),
            "features": p.features or []
        }
        for p in plans
    ]

@router.post("/create-order")
async def create_payment_order(req: CreateOrderRequest, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    plan = db.query(models.Plan).filter(models.Plan.id == req.plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    receipt_str = f"usr_{current_user.id}"
    order_data = await create_razorpay_order(float(plan.price_inr), receipt_id=receipt_str)

    sub_id = None
    if current_user.role == models.UserRole.recruiter:
        recruiter = db.query(models.Recruiter).filter(models.Recruiter.user_id == current_user.id).first()
        if not recruiter:
            recruiter = models.Recruiter(user_id=current_user.id, company_name="Recruiter Enterprise")
            db.add(recruiter)
            db.flush()

        sub = db.query(models.Subscription).filter(models.Subscription.recruiter_id == recruiter.id).first()
        if not sub:
            sub = models.Subscription(
                recruiter_id=recruiter.id,
                plan_id=plan.id,
                credits_remaining=plan.monthly_credits,
                status=models.SubscriptionStatus.active
            )
            db.add(sub)
            db.flush()
        sub_id = sub.id

    tx = models.Transaction(
        subscription_id=sub_id,
        user_id=current_user.id,
        razorpay_order_id=order_data["id"],
        amount_inr=plan.price_inr,
        plan_name=plan.plan_name,
        status=models.TransactionStatus.pending
    )
    db.add(tx)
    db.commit()

    return {
        "order_id": order_data["id"],
        "amount": order_data["amount"],
        "currency": order_data["currency"],
        "key_id": order_data["key_id"],
        "plan_name": plan.plan_name,
        "tier": plan.tier.value,
        "monthly_credits": plan.monthly_credits,
        "price_inr": float(plan.price_inr),
        "features": plan.features or [],
        "has_real_razorpay": bool(settings.RAZORPAY_KEY_ID and not settings.RAZORPAY_KEY_ID.startswith("rzp_test_mock"))
    }

@router.post("/process-inapp-payment")
def process_inapp_payment(req: ProcessInAppPaymentRequest, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    plan = db.query(models.Plan).filter(models.Plan.id == req.plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    tx = db.query(models.Transaction).filter(models.Transaction.razorpay_order_id == req.order_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Order not found")

    import uuid
    payment_id = f"pay_{uuid.uuid4().hex[:14]}"
    sig = generate_inapp_payment_signature(req.order_id, payment_id)

    # Method description
    method_str = "Card"
    if req.payment_method == "upi":
        method_str = f"UPI ({req.upi_vpa or 'Instant QR'})"
    elif req.payment_method == "netbanking":
        method_str = f"NetBanking ({req.bank_name or 'Bank Transfer'})"
    elif req.card_last4:
        method_str = f"Card ending in {req.card_last4}"

    tx.razorpay_payment_id = payment_id
    tx.payment_method = method_str
    tx.plan_name = plan.plan_name
    tx.status = models.TransactionStatus.success

    credits_rem = 0
    if current_user.role == models.UserRole.recruiter:
        sub = db.query(models.Subscription).filter(models.Subscription.id == tx.subscription_id).first() if tx.subscription_id else None
        if not sub:
            recruiter = db.query(models.Recruiter).filter(models.Recruiter.user_id == current_user.id).first()
            if recruiter:
                sub = db.query(models.Subscription).filter(models.Subscription.recruiter_id == recruiter.id).first()
        if sub:
            sub.plan_id = plan.id
            sub.credits_remaining += plan.monthly_credits
            sub.status = models.SubscriptionStatus.active
            credits_rem = sub.credits_remaining

            ledger = models.CreditLedger(
                subscription_id=sub.id,
                action=f"Upgraded to {plan.plan_name} via {method_str} (+{plan.monthly_credits} credits)",
                credits_used=0
            )
            db.add(ledger)
    else:
        # Student upgrade
        sp = current_user.student_profile
        if not sp:
            sp = models.StudentProfile(user_id=current_user.id, is_eligible=True)
            db.add(sp)
        sp.is_premium = True

    db.commit()

    return {
        "status": "success",
        "message": f"Payment Authorized! Successfully upgraded to {plan.plan_name}.",
        "tier": plan.tier.value,
        "plan_name": plan.plan_name,
        "credits_remaining": credits_rem,
        "payment_id": payment_id,
        "order_id": req.order_id,
        "amount_inr": float(tx.amount_inr),
        "payment_method": method_str,
        "signature": sig,
        "paid_at": datetime.now(timezone.utc).isoformat()
    }

@router.post("/verify")
def verify_payment(req: VerifyPaymentRequest, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # CRITICAL SECURITY RULE: Verify HMAC-SHA256 signature server-side
    is_valid = verify_razorpay_signature(req.razorpay_order_id, req.razorpay_payment_id, req.razorpay_signature)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid payment signature verification failed")

    tx = db.query(models.Transaction).filter(models.Transaction.razorpay_order_id == req.razorpay_order_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction order not found")

    plan = db.query(models.Plan).filter(models.Plan.id == req.plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    sub = db.query(models.Subscription).filter(models.Subscription.id == tx.subscription_id).first()

    tx.razorpay_payment_id = req.razorpay_payment_id
    tx.status = models.TransactionStatus.success

    if sub:
        sub.plan_id = plan.id
        sub.credits_remaining += plan.monthly_credits
        sub.status = models.SubscriptionStatus.active

        # Log credit ledger entry
        ledger = models.CreditLedger(
            subscription_id=sub.id,
            action=f"Plan top-up / upgrade to {plan.plan_name} (+{plan.monthly_credits} credits)",
            credits_used=0
        )
        db.add(ledger)

    db.commit()

    return {
        "status": "success",
        "message": f"Payment verified! Upgraded to {plan.plan_name}. Added {plan.monthly_credits} credits.",
        "tier": plan.tier.value,
        "plan_name": plan.plan_name,
        "credits_remaining": sub.credits_remaining if sub else 0,
        "transaction_id": tx.razorpay_payment_id,
        "amount_inr": float(tx.amount_inr),
        "order_id": tx.razorpay_order_id
    }

@router.post("/direct-upgrade")
def direct_upgrade_plan(req: DirectUpgradeRequest, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != models.UserRole.recruiter:
        raise HTTPException(status_code=403, detail="Recruiter role required to upgrade plan")

    plan = db.query(models.Plan).filter(models.Plan.id == req.plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    recruiter = db.query(models.Recruiter).filter(models.Recruiter.user_id == current_user.id).first()
    if not recruiter:
        recruiter = models.Recruiter(user_id=current_user.id, company_name="Default Corp")
        db.add(recruiter)
        db.flush()

    sub = db.query(models.Subscription).filter(models.Subscription.recruiter_id == recruiter.id).first()
    if not sub:
        sub = models.Subscription(
            recruiter_id=recruiter.id,
            plan_id=plan.id,
            credits_remaining=plan.monthly_credits,
            status=models.SubscriptionStatus.active
        )
        db.add(sub)
    else:
        sub.plan_id = plan.id
        sub.credits_remaining += plan.monthly_credits
        sub.status = models.SubscriptionStatus.active

    # Log completed transaction
    tx = models.Transaction(
        subscription_id=sub.id,
        razorpay_order_id=f"direct_order_{int(datetime.now(timezone.utc).timestamp())}",
        razorpay_payment_id=f"direct_pay_{int(datetime.now(timezone.utc).timestamp())}",
        amount_inr=plan.price_inr,
        status=models.TransactionStatus.success
    )
    db.add(tx)

    # Log credit ledger entry
    ledger = models.CreditLedger(
        subscription_id=sub.id,
        action=f"Upgraded to {plan.plan_name} (+{plan.monthly_credits} credits)",
        credits_used=0
    )
    db.add(ledger)
    db.commit()

    return {
        "status": "success",
        "message": f"Successfully upgraded to {plan.plan_name}! Added {plan.monthly_credits} credits.",
        "tier": plan.tier.value,
        "credits_remaining": sub.credits_remaining
    }

@router.get("/my-subscription")
def get_my_subscription(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role == models.UserRole.recruiter:
        recruiter = db.query(models.Recruiter).filter(models.Recruiter.user_id == current_user.id).first()
        sub = None
        if recruiter:
            sub = db.query(models.Subscription).filter(
                models.Subscription.recruiter_id == recruiter.id,
                models.Subscription.status == models.SubscriptionStatus.active
            ).first()

        plan_name = sub.plan.plan_name if (sub and sub.plan) else "Free Tier"
        tier = sub.plan.tier.value if (sub and sub.plan) else "free"
        credits_rem = sub.credits_remaining if sub else 0
        return {
            "tier": tier,
            "plan_name": plan_name,
            "credits_remaining": credits_rem,
            "status": "active"
        }
    else:
        sp = current_user.student_profile
        is_prem = bool(sp and sp.is_premium)
        return {
            "tier": "premium" if is_prem else "free",
            "plan_name": "CareerPilot Student Pro" if is_prem else "Free Student Plan",
            "is_premium": is_prem,
            "credits_remaining": 0,
            "status": "active"
        }

@router.get("/history")
def get_payment_history(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    txs = []
    if current_user.role == models.UserRole.recruiter:
        recruiter = db.query(models.Recruiter).filter(models.Recruiter.user_id == current_user.id).first()
        sub = db.query(models.Subscription).filter(models.Subscription.recruiter_id == recruiter.id).first() if recruiter else None
        if sub:
            txs = db.query(models.Transaction).filter(
                (models.Transaction.subscription_id == sub.id) | (models.Transaction.user_id == current_user.id)
            ).order_by(models.Transaction.created_at.desc()).all()
        else:
            txs = db.query(models.Transaction).filter(models.Transaction.user_id == current_user.id).order_by(models.Transaction.created_at.desc()).all()
    else:
        txs = db.query(models.Transaction).filter(models.Transaction.user_id == current_user.id).order_by(models.Transaction.created_at.desc()).all()

    return [
        {
            "id": str(t.id),
            "order_id": t.razorpay_order_id,
            "payment_id": t.razorpay_payment_id or t.razorpay_order_id,
            "amount": float(t.amount_inr),
            "amount_inr": float(t.amount_inr),
            "plan_name": t.plan_name or "Subscription Plan",
            "payment_method": t.payment_method or "Razorpay Gateway",
            "status": t.status.value,
            "created_at": t.created_at.isoformat() if t.created_at else None,
            "invoice_no": f"INV-2026-{str(t.id)[:8].upper()}"
        }
        for t in txs
    ]

@router.get("/credit-ledger")
def get_credit_ledger_history(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != models.UserRole.recruiter:
        return []

    recruiter = db.query(models.Recruiter).filter(models.Recruiter.user_id == current_user.id).first()
    if not recruiter:
        return []

    sub = db.query(models.Subscription).filter(models.Subscription.recruiter_id == recruiter.id).first()
    if not sub:
        return []

    ledger = db.query(models.CreditLedger).filter(models.CreditLedger.subscription_id == sub.id).order_by(models.CreditLedger.created_at.desc()).all()
    return [
        {
            "id": str(l.id),
            "description": l.action,
            "amount": -l.credits_used if l.credits_used > 0 else 0,
            "credits_used": l.credits_used,
            "created_at": l.created_at.isoformat() if l.created_at else None
        }
        for l in ledger
    ]

@router.get("/billing-history")
def get_billing_history(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    recruiter = db.query(models.Recruiter).filter(models.Recruiter.user_id == current_user.id).first()
    if not recruiter:
        return {"transactions": [], "credit_ledger": []}

    sub = db.query(models.Subscription).filter(models.Subscription.recruiter_id == recruiter.id).first()
    if not sub:
        return {"transactions": [], "credit_ledger": []}

    txs = db.query(models.Transaction).filter(models.Transaction.subscription_id == sub.id).order_by(models.Transaction.created_at.desc()).all()
    ledger = db.query(models.CreditLedger).filter(models.CreditLedger.subscription_id == sub.id).order_by(models.CreditLedger.created_at.desc()).all()

    return {
        "credits_remaining": sub.credits_remaining,
        "plan_name": sub.plan.plan_name if sub.plan else "Free",
        "tier": sub.plan.tier.value if sub.plan else "free",
        "transactions": [
            {
                "id": str(t.id),
                "razorpay_order_id": t.razorpay_order_id,
                "razorpay_payment_id": t.razorpay_payment_id,
                "amount_inr": float(t.amount_inr),
                "status": t.status.value,
                "created_at": t.created_at.isoformat() if t.created_at else None
            }
            for t in txs
        ],
        "credit_ledger": [
            {
                "id": str(l.id),
                "action": l.action,
                "credits_used": l.credits_used,
                "created_at": l.created_at.isoformat() if l.created_at else None
            }
            for l in ledger
        ]
    }

class StudentUpgradeRequest(BaseModel):
    payment_method: Optional[str] = "upi"

@router.post("/student/upgrade")
def upgrade_student_pro(req: StudentUpgradeRequest = None, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != models.UserRole.student:
        raise HTTPException(status_code=403, detail="Student role required")

    sp = current_user.student_profile
    if not sp:
        sp = models.StudentProfile(user_id=current_user.id, is_eligible=True)
        db.add(sp)

    sp.is_premium = True

    import uuid
    order_id = f"stu_order_{int(datetime.now(timezone.utc).timestamp())}"
    payment_id = f"pay_stu_{uuid.uuid4().hex[:12]}"

    p_method = (req.payment_method if req else "upi") or "upi"
    method_name = "UPI Instant Transfer" if p_method == "upi" else ("Credit/Debit Card" if p_method == "card" else "NetBanking")

    tx = models.Transaction(
        user_id=current_user.id,
        razorpay_order_id=order_id,
        razorpay_payment_id=payment_id,
        amount_inr=499.00,
        plan_name="CareerPilot Student Pro",
        payment_method=method_name,
        status=models.TransactionStatus.success
    )
    db.add(tx)
    db.commit()

    return {
        "status": "success",
        "message": "Congratulations! You have upgraded to CareerPilot Student Pro.",
        "is_premium": True,
        "plan_name": "CareerPilot Student Pro",
        "order_id": order_id,
        "payment_id": payment_id,
        "amount_inr": 499.00,
        "paid_at": datetime.now(timezone.utc).isoformat()
    }
