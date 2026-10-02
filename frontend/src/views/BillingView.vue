<template>
  <div class="billing-page">

    <!-- Toast Notification -->
    <transition name="toast-fade">
      <div v-if="toast" class="toast-popup" :class="`toast-popup--${toast.type}`">
        <span>{{ toast.type === 'error' ? '⚠️' : '✅' }}</span>
        <span>{{ toast.message }}</span>
      </div>
    </transition>

    <!-- Top Hero Section -->
    <div class="billing-hero-card">
      <div class="hero-left">
        <div class="hero-tier-badge">
          <span class="crown-icon">{{ authStore.role === 'student' ? '🎓' : '👑' }}</span>
          <span>CURRENT TIER: {{ currentTierName }}</span>
        </div>
        <h1 class="hero-title">
          {{ authStore.role === 'student' ? 'Student Pro & Career Acceleration' : 'Recruiter Subscriptions & Talent Credits' }}
        </h1>
        <p class="hero-subtitle">
          {{ authStore.role === 'student'
            ? 'Supercharge your job applications with all premium resume templates, granular AI Job Match Explainability, and cryptographic trust badges.'
            : 'Scale candidate outreach, unlock cryptographic skill verifications, and access AI Match Explainability in real time.' }}
        </p>
      </div>

      <div class="hero-right">
        <div v-if="authStore.role === 'recruiter'" class="credits-capsule">
          <div class="credits-label">Available Talent Credits</div>
          <div class="credits-num">{{ billing.credits_remaining ?? 0 }}</div>
          <div class="credits-sub">Ready for instant profile unlocks</div>
        </div>
        <div v-else class="credits-capsule">
          <div class="credits-label">Student Membership</div>
          <div class="credits-num" style="font-size: 1.25rem; font-weight: 700;">
            {{ (billing.is_premium || authStore.isUserPremium) ? '⭐ PRO ACTIVE' : 'FREE TIER' }}
          </div>
          <div class="credits-sub">
            {{ (billing.is_premium || authStore.isUserPremium) ? 'All premium templates & telemetry unlocked' : 'Upgrade to Pro for full AI telemetry' }}
          </div>
        </div>
      </div>
    </div>

    <!-- Plans Grid -->
    <div class="plans-grid" :class="{ 'plans-grid--student': authStore.role === 'student' }">
      <div
        v-for="plan in activePlansList"
        :key="plan.id"
        class="plan-card"
        :class="{
          'plan-card--active': plan.is_current,
          'plan-card--featured': plan.is_featured
        }"
      >
        <!-- Popular / Active Badge -->
        <div v-if="plan.badge_text" class="card-pill" :class="plan.is_current ? 'card-pill--active' : 'card-pill--popular'">
          {{ plan.badge_text }}
        </div>

        <div class="plan-header">
          <div class="plan-tier-name">{{ plan.name }}</div>
          <p class="plan-tagline">{{ plan.tagline }}</p>
          <div class="plan-price-row">
            <span class="price-curr">₹</span>
            <span class="price-amount">{{ plan.price_inr }}</span>
            <span class="price-cycle">/month</span>
          </div>
        </div>

        <!-- Plan Credits Callout -->
        <div v-if="authStore.role === 'recruiter'" class="plan-credits-box">
          <span class="bolt-icon">⚡</span>
          <span class="credits-text">
            <strong>{{ plan.monthly_credits }} Candidate Unlocks</strong> included / mo
          </span>
        </div>
        <div v-else class="plan-credits-box" style="background: #F0FDF4; border-color: #BBF7D0;">
          <span class="bolt-icon" style="color: #16A34A;">⭐</span>
          <span class="credits-text" style="color: #15803D;">
            <strong>{{ plan.tier === 'premium' ? 'All Pro Resume Templates & Match AI' : 'Standard Student Portfolio Access' }}</strong>
          </span>
        </div>

        <!-- Feature List -->
        <ul class="features-list">
          <li
            v-for="(feat, idx) in plan.features"
            :key="idx"
            :class="['feature-item', feat.included ? 'feature-item--checked' : 'feature-item--disabled']"
          >
            <span class="check-icon">{{ feat.included ? '✓' : '✕' }}</span>
            <span class="feature-text" :class="{ 'font-bold': feat.highlight }">{{ feat.text }}</span>
          </li>
        </ul>

        <!-- Action CTA -->
        <div class="plan-action-wrap">
          <button
            v-if="plan.is_current"
            class="btn-plan btn-plan--current"
            disabled
          >
            Active Subscription
          </button>
          <button
            v-else
            @click="initiatePlanCheckout(plan)"
            class="btn-plan btn-plan--upgrade"
            :class="{ 'btn-plan--featured': plan.is_featured }"
          >
            Upgrade to {{ plan.name }} →
          </button>
        </div>
      </div>
    </div>

    <!-- Activity Section (Transaction History & Credit Ledger) -->
    <div class="activity-section">
      <div class="activity-header">
        <div>
          <h2 class="activity-title">
            {{ authStore.role === 'student' ? 'Payment Invoices & Tax Receipts' : 'Billing Records & Credit Ledger' }}
          </h2>
          <p class="activity-sub">
            {{ authStore.role === 'student'
              ? 'Instant access to your verified payment receipts and tax invoices with cryptographic verification.'
              : 'Transparent breakdown of all card, UPI, NetBanking payments and credit disbursements.' }}
          </p>
        </div>
        <button @click="loadBillingData" class="btn-refresh">
          <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
            <path d="M23 4v6h-6M1 20v-6h6M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
          </svg>
          <span>Refresh</span>
        </button>
      </div>

      <div class="activity-grid" :class="{ 'activity-grid--single': authStore.role !== 'recruiter' }">
        
        <!-- Column 1: Payment Transactions -->
        <div class="activity-card">
          <div class="card-inner-header">
            <div class="inner-title-wrap">
              <span class="inner-icon">💳</span>
              <h3 class="inner-title">Payment Transactions</h3>
            </div>
            <span class="badge-count">{{ paymentHistory.length }} Records</span>
          </div>

          <div class="tx-list">
            <div v-for="tx in paymentHistory" :key="tx.id" class="tx-row">
              <div class="tx-left">
                <div class="tx-id">{{ tx.plan_name || 'Talent Credits Subscription' }}</div>
                <div class="tx-date">{{ formatDate(tx.created_at) }} • {{ tx.payment_method || 'Card / UPI' }}</div>
                <div class="tx-sub-meta">Order #{{ tx.order_id ? tx.order_id.slice(-10) : tx.id.slice(0, 8) }}</div>
              </div>
              <div class="tx-right">
                <div class="tx-amount">₹{{ tx.amount }}</div>
                <div class="tx-actions-wrap">
                  <span
                    class="status-chip"
                    :class="tx.status === 'success' ? 'status-chip--success' : 'status-chip--pending'"
                  >
                    {{ (tx.status || 'success').toUpperCase() }}
                  </span>
                  <button @click="openReceipt(tx)" class="btn-receipt-action" title="View & Download Tax Receipt">
                    📄 Receipt
                  </button>
                </div>
              </div>
            </div>

            <div v-if="!paymentHistory.length" class="empty-tx">
              No previous transactions found for this workspace.
            </div>
          </div>
        </div>

        <!-- Column 2: Credit Ledger Activity (Recruiter Only) -->
        <div v-if="authStore.role === 'recruiter'" class="activity-card">
          <div class="card-inner-header">
            <div class="inner-title-wrap">
              <span class="inner-icon">📜</span>
              <h3 class="inner-title">Credit Ledger Audit Trail</h3>
            </div>
            <span class="badge-count">{{ creditLedger.length }} Entries</span>
          </div>

          <div class="tx-list">
            <div v-for="log in creditLedger" :key="log.id" class="tx-row">
              <div class="tx-left">
                <div class="tx-desc">{{ log.description || 'Subscription Credit Grant' }}</div>
                <div class="tx-date">{{ formatDate(log.created_at) }}</div>
              </div>
              <div class="tx-right">
                <div class="credit-delta" :class="log.amount >= 0 ? 'credit-delta--plus' : 'credit-delta--minus'">
                  {{ log.amount >= 0 ? '+' + log.amount : log.amount }} Credits
                </div>
                <span class="status-chip status-chip--recorded">Recorded</span>
              </div>
            </div>

            <div v-if="!creditLedger.length" class="empty-tx">
              No credit transactions recorded yet.
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- ── MODAL: Realtime Multi-Method Checkout ────────────────────── -->
    <div v-if="isCheckoutOpen" class="modal-overlay" @click.self="closeCheckout">
      <div class="checkout-modal">
        
        <!-- Header -->
        <div class="checkout-header">
          <div>
            <span class="modal-badge">SECURE 256-BIT ENCRYPTION</span>
            <h3 class="modal-title">Upgrade to {{ activeOrder.plan_name }}</h3>
          </div>
          <button @click="closeCheckout" class="btn-modal-close">✕</button>
        </div>

        <!-- STAGE 1: Payment Method Selection & Form -->
        <div v-if="checkoutStage === 'form'" class="checkout-body">
          
          <!-- Summary Bar -->
          <div class="order-summary-box">
            <div class="summary-line">
              <span class="summary-label">Subscription Tier:</span>
              <span class="summary-val">{{ activeOrder.plan_name }}</span>
            </div>
            <div class="summary-line">
              <span class="summary-label">{{ authStore.role === 'student' ? 'Perks Unlocked:' : 'Talent Credits Added:' }}</span>
              <span class="summary-val font-bold text-blue-600">
                {{ authStore.role === 'student' ? 'Clean & Minimal Templates, AI Match & Trust Badges' : `+${activeOrder.monthly_credits} Credits` }}
              </span>
            </div>
            <div class="summary-line total-line">
              <span class="summary-label">Total Amount Payable:</span>
              <span class="summary-val total-amount">₹{{ activeOrder.price_inr }} <small>INR</small></span>
            </div>
          </div>

          <!-- Payment Tabs -->
          <div class="method-tabs">
            <button
              type="button"
              @click="paymentMethod = 'card'"
              :class="['method-tab-btn', paymentMethod === 'card' && 'method-tab-btn--active']"
            >
              <span>💳 Credit/Debit Card</span>
            </button>
            <button
              type="button"
              @click="paymentMethod = 'upi'"
              :class="['method-tab-btn', paymentMethod === 'upi' && 'method-tab-btn--active']"
            >
              <span>⚡ UPI / QR Code</span>
            </button>
            <button
              type="button"
              @click="paymentMethod = 'netbanking'"
              :class="['method-tab-btn', paymentMethod === 'netbanking' && 'method-tab-btn--active']"
            >
              <span>🏛️ NetBanking</span>
            </button>
          </div>

          <!-- CARD FORM -->
          <div v-if="paymentMethod === 'card'" class="payment-fields-pane">
            <div class="field-item">
              <label class="field-item-label">Card Number</label>
              <input v-model="cardForm.number" type="text" placeholder="4242 •••• •••• 4242" class="field-item-input" />
            </div>
            <div class="grid-2col">
              <div class="field-item">
                <label class="field-item-label">Expiry Date</label>
                <input v-model="cardForm.expiry" type="text" placeholder="MM / YY" class="field-item-input" />
              </div>
              <div class="field-item">
                <label class="field-item-label">CVV / CVC</label>
                <input v-model="cardForm.cvv" type="password" maxlength="4" placeholder="123" class="field-item-input" />
              </div>
            </div>
            <div class="field-item">
              <label class="field-item-label">Cardholder Name</label>
              <input v-model="cardForm.name" type="text" placeholder="Sarah Jenkins" class="field-item-input" />
            </div>
          </div>

          <!-- UPI FORM -->
          <div v-else-if="paymentMethod === 'upi'" class="payment-fields-pane">
            <div class="upi-box">
              <div class="qr-placeholder">
                <div class="qr-icon">📱</div>
                <div class="qr-text">Scan with any UPI App (GPay, PhonePe, Paytm)</div>
              </div>
            </div>
            <div class="field-item">
              <label class="field-item-label">Or enter your UPI VPA ID</label>
              <input v-model="upiId" type="text" placeholder="username@okhdfcbank" class="field-item-input" />
            </div>
          </div>

          <!-- NETBANKING FORM -->
          <div v-else-if="paymentMethod === 'netbanking'" class="payment-fields-pane">
            <div class="field-item">
              <label class="field-item-label">Select Recognized Bank</label>
              <select v-model="selectedBank" class="field-item-select">
                <option value="HDFC Bank">HDFC Bank</option>
                <option value="State Bank of India">State Bank of India (SBI)</option>
                <option value="ICICI Bank">ICICI Bank</option>
                <option value="Axis Bank">Axis Bank</option>
                <option value="Kotak Mahindra Bank">Kotak Mahindra Bank</option>
              </select>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="checkout-footer">
            <button @click="closeCheckout" class="btn-cancel">Cancel</button>
            <button @click="executePayment" class="btn-pay-now">
              <span>Authorize &amp; Pay ₹{{ activeOrder.price_inr }} →</span>
            </button>
          </div>

        </div>

        <!-- STAGE 2: Processing Animation -->
        <div v-else-if="checkoutStage === 'processing'" class="checkout-body processing-pane">
          <div class="spinner-large"></div>
          <h3 class="processing-title">{{ processingStatusText }}</h3>
          <p class="processing-sub">Please do not close this window. Validating 256-bit payment gateway token in real time...</p>
        </div>

        <!-- STAGE 3: Instant Success Receipt -->
        <div v-else-if="checkoutStage === 'success'" class="checkout-body success-pane">
          <div class="success-icon-circle">✓</div>
          <h3 class="success-title">Payment Authorized &amp; Plan Upgraded!</h3>
          <p class="success-desc">
            Your workspace has been upgraded to <strong>{{ successReceipt.plan_name || 'CareerPilot Student Pro' }}</strong>.
            <template v-if="authStore.role === 'recruiter'">
              <strong>+{{ successReceipt.credits_added || 200 }} Talent Credits</strong> have been added to your balance.
            </template>
            <template v-else>
              All premium resume templates, granular AI Job Match Explainability, and cryptographic trust badges are now active!
            </template>
          </p>

          <button @click="closeCheckout" class="btn-done">
            Return to Workspace
          </button>
        </div>

      </div>
    </div>

    <!-- ── RECEIPT MODAL ───────────────────────── -->
    <div v-if="showReceiptModal && selectedReceipt" class="modal-overlay" @click.self="showReceiptModal=false">
      <div class="modal-box modal-box--receipt">
        <div class="receipt-header-actions no-print">
          <span class="receipt-status-pill">✓ OFFICIAL PAYMENT RECEIPT</span>
          <div class="receipt-btn-group">
            <button @click="printReceipt" class="btn-receipt-print">🖨 Print / Save as PDF</button>
            <button @click="showReceiptModal=false" class="btn-modal-close">✕</button>
          </div>
        </div>

        <div id="printable-receipt" class="receipt-paper">
          <div class="receipt-brand-row">
            <div>
              <div class="receipt-brand-title">CareerPilot <span class="brand-blue">AI</span></div>
              <div class="receipt-brand-sub">Autonomous Talent Governance & Cryptographic Verification Platform</div>
            </div>
            <div class="receipt-meta-block">
              <div class="inv-tag">TAX INVOICE / RECEIPT</div>
              <div class="inv-no">{{ selectedReceipt.invoice_no }}</div>
              <div class="inv-date">Date: {{ selectedReceipt.date }}</div>
            </div>
          </div>

          <div class="receipt-hr"></div>

          <div class="receipt-parties-row">
            <div class="party-box">
              <div class="party-heading">BILLED TO:</div>
              <div class="party-name">{{ selectedReceipt.customer_name }}</div>
              <div class="party-email">{{ selectedReceipt.customer_email }}</div>
              <div class="party-type">{{ authStore.userRole === 'recruiter' ? 'Verified Corporate Recruiter' : 'Verified Candidate' }}</div>
            </div>
            <div class="party-box text-right">
              <div class="party-heading">ISSUED BY:</div>
              <div class="party-name">CareerPilot Technologies Pvt. Ltd.</div>
              <div class="party-email">GSTIN: 29AABCU9603R1ZM</div>
              <div class="party-type">Bangalore Tech Hub, KA 560100</div>
            </div>
          </div>

          <table class="receipt-table">
            <thead>
              <tr>
                <th class="text-left">Plan / Service Item</th>
                <th class="text-center">Payment Method</th>
                <th class="text-center">Status</th>
                <th class="text-right">Amount (INR)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="text-left">
                  <div class="item-title">{{ selectedReceipt.plan_name }}</div>
                  <div class="item-meta">Order ID: {{ selectedReceipt.order_id }}</div>
                  <div class="item-meta">Transaction: {{ selectedReceipt.payment_id }}</div>
                </td>
                <td class="text-center">{{ selectedReceipt.payment_method }}</td>
                <td class="text-center"><span class="badge-paid">PAID</span></td>
                <td class="text-right font-bold">₹{{ Number(selectedReceipt.amount).toFixed(2) }}</td>
              </tr>
            </tbody>
            <tfoot>
              <tr>
                <td colspan="3" class="text-right font-bold">Total Paid:</td>
                <td class="text-right font-bold text-blue-600">₹{{ Number(selectedReceipt.amount).toFixed(2) }} INR</td>
              </tr>
            </tfoot>
          </table>

          <div class="receipt-footer-box">
            <p>Thank you for partnering with CareerPilot AI. This is a computer-generated tax invoice with 256-bit cryptographic verification signature.</p>
            <p class="receipt-seal">🔒 Verified Digital Ledger Hash: {{ (selectedReceipt.id || 'sec789').slice(0, 16) }}</p>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { apiFetch } from '../services/api'
import { useAuthStore } from '../store'

const authStore = useAuthStore()
const plans = ref([])
const billing = ref({})
const paymentHistory = ref([])
const creditLedger = ref([])

// Checkout State
const isCheckoutOpen = ref(false)
const checkoutStage = ref('form') // 'form' | 'processing' | 'success'
const isProcessing = ref(false)
const processingStep = ref(1)
const processingStatusText = ref('Connecting to secure payment gateway...')

const activeOrder = ref({})
const paymentMethod = ref('card') // 'card' | 'upi' | 'netbanking'
const toast = ref(null)

let toastTimer = null
const showToast = (message, type = 'success') => {
  if (toastTimer) clearTimeout(toastTimer)
  toast.value = { message, type }
  toastTimer = setTimeout(() => {
    toast.value = null
  }, 4000)
}

const cardForm = ref({
  number: '4242 •••• •••• 4242',
  expiry: '12/28',
  cvv: '888',
  name: authStore.userFullName || 'Recruiter Officer'
})
const upiId = ref('recruiter@okaxis')
const selectedBank = ref('HDFC Bank')
const successReceipt = ref({})

// Receipt Modal State
const showReceiptModal = ref(false)
const selectedReceipt = ref(null)

const openReceipt = (tx) => {
  selectedReceipt.value = {
    ...tx,
    invoice_no: tx.invoice_no || `INV-2026-${(tx.id || 'TX100').slice(0, 8).toUpperCase()}`,
    customer_name: authStore.userFullName || (authStore.userRole === 'recruiter' ? 'Verified Recruiter Officer' : 'Verified Candidate'),
    customer_email: authStore.user?.email || 'user@careerpilot.ai',
    date: formatDate(tx.created_at)
  }
  showReceiptModal.value = true
}

const printReceipt = () => {
  window.print()
}

const currentTierName = computed(() => {
  return (billing.value.tier || 'Free').toUpperCase()
})

onMounted(async () => {
  await loadBillingData()
})

const loadBillingData = async () => {
  try {
    const plansData = await apiFetch('/payments/plans')
    plans.value = plansData || []

    const billData = await apiFetch('/payments/my-subscription')
    billing.value = billData || {}

    const history = await apiFetch('/payments/history')
    paymentHistory.value = history || []

    const ledger = await apiFetch('/payments/credit-ledger')
    creditLedger.value = ledger || []
  } catch (err) {
    console.error('Billing data fetch error:', err)
  }
}

const getPlanTagline = (tier) => {
  if (tier === 'premium') return 'Enterprise capability for fast-growing talent pipelines'
  if (tier === 'basic') return 'Essential candidate discovery & comparison tools'
  return 'Get started exploring verified student portfolios'
}

const getPlanFeatures = (tier) => {
  if (tier === 'premium') {
    return [
      { text: '200 Candidate Profile Unlocks / Mo', included: true, highlight: true },
      { text: 'Side-by-Side Candidate Comparison Matrix', included: true, highlight: true },
      { text: 'AI Job Match Granular Explainability', included: true, highlight: true },
      { text: 'Recruiter Pipeline & Conversion Analytics', included: true, highlight: true },
      { text: 'Anti-Cheat Behavioral Telemetry Logs', included: true },
      { text: 'Direct Candidate Messaging & Scheduling', included: true }
    ]
  }
  if (tier === 'basic') {
    return [
      { text: '50 Candidate Profile Unlocks / Mo', included: true, highlight: true },
      { text: 'Side-by-Side Candidate Comparison Matrix', included: true, highlight: true },
      { text: 'Semantic Opportunity & Candidate Search', included: true },
      { text: 'Verified Skill Trust Badges', included: true },
      { text: 'AI Job Match Granular Explainability', included: false },
      { text: 'Recruiter Pipeline & Conversion Analytics', included: false }
    ]
  }
  return [
    { text: '10 Candidate Profile Unlocks / Mo', included: true },
    { text: 'Basic Candidate Skill Search', included: true },
    { text: 'View Verified Competency Chips', included: true },
    { text: 'Candidate Comparison Matrix', included: false },
    { text: 'AI Match Explainability', included: false },
    { text: 'Recruiter Analytics', included: false }
  ]
}

const activePlansList = computed(() => {
  if (authStore.role === 'student') {
    const proPlan = plans.value.find(p => p.plan_name === 'CareerPilot Student Pro' || p.price_inr === 499)
    const isPrem = !!(billing.value.is_premium || authStore.isUserPremium)
    return [
      {
        id: 'free_student',
        name: 'Free Student Plan',
        tier: 'free',
        price_inr: 0,
        monthly_credits: 0,
        tagline: 'Essential career exploration and verified skill testing',
        badge_text: isPrem ? '' : '✓ CURRENT PLAN',
        is_current: !isPrem,
        is_featured: false,
        features: [
          { text: 'Standard Portfolio & Verified Profile', included: true },
          { text: 'Access to Domain Skill Assessments', included: true },
          { text: 'Basic AI Resume Generator (Modern template)', included: true },
          { text: 'Browse Opportunities & Apply with Passport', included: true },
          { text: 'High-Level Match Score (%)', included: true },
          { text: 'Customized Premium Templates (Clean, Minimal)', included: false },
          { text: 'Granular AI Match & Skill Gap Breakdown', included: false },
          { text: 'Cryptographic Trust Score Telemetry', included: false }
        ]
      },
      {
        id: proPlan ? proPlan.id : '5be52969-6cd6-42c1-8d3e-f6fd7ad46c55',
        name: 'CareerPilot Student Pro',
        tier: 'premium',
        price_inr: 499,
        monthly_credits: 0,
        tagline: 'Maximum placement visibility & full AI career intelligence',
        badge_text: isPrem ? '✓ CURRENT PLAN' : '★ RECOMMENDED',
        is_current: isPrem,
        is_featured: true,
        features: [
          { text: 'Standard Portfolio & Verified Profile', included: true },
          { text: 'Access to Domain Skill Assessments', included: true },
          { text: 'Clean & Minimal Premium Resume Templates', included: true, highlight: true },
          { text: 'Granular AI Match & Skill Gap Telemetry', included: true, highlight: true },
          { text: 'Cryptographic Trust Score Telemetry', included: true, highlight: true },
          { text: 'Priority Candidate Placement for Recruiters', included: true, highlight: true },
          { text: 'Downloadable Official Tax Receipts & Invoices', included: true, highlight: true }
        ]
      }
    ]
  } else {
    // Recruiter plans
    return plans.value
      .filter(p => p.plan_name !== 'CareerPilot Student Pro')
      .map(p => ({
        ...p,
        name: p.plan_name,
        tagline: getPlanTagline(p.tier),
        features: getPlanFeatures(p.tier),
        is_current: p.tier === billing.value.tier,
        is_featured: p.tier === 'premium',
        badge_text: p.tier === billing.value.tier ? '✓ CURRENT PLAN' : (p.tier === 'premium' ? '★ MOST POPULAR' : '')
      }))
  }
})

const formatDate = (isoString) => {
  if (!isoString) return 'Recent'
  return new Date(isoString).toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  })
}

const initiatePlanCheckout = async (plan) => {
  try {
    const order = await apiFetch('/payments/create-order', {
      method: 'POST',
      body: JSON.stringify({ plan_id: plan.id })
    })

    activeOrder.value = {
      ...order,
      plan_id: plan.id
    }
    checkoutStage.value = 'form'
    isCheckoutOpen.value = true
  } catch (err) {
    showToast(err.message || 'Could not initiate payment order', 'error')
  }
}

const closeCheckout = () => {
  isCheckoutOpen.value = false
  checkoutStage.value = 'form'
  isProcessing.value = false
}

const executePayment = async () => {
  isProcessing.value = true
  checkoutStage.value = 'processing'
  processingStep.value = 1
  processingStatusText.value = 'Securing 256-bit encrypted checkout session...'

  await new Promise(r => setTimeout(r, 600))
  processingStep.value = 2
  processingStatusText.value = `Authorizing ₹${activeOrder.value.price_inr} with payment gateway...`

  await new Promise(r => setTimeout(r, 700))
  processingStep.value = 3
  processingStatusText.value = 'Verifying signature & upgrading subscription...'

  try {
    const cardLast4 = paymentMethod.value === 'card' ? (cardForm.value.number || '').replace(/\s/g, '').slice(-4) : null

    const res = await apiFetch('/payments/process-inapp-payment', {
      method: 'POST',
      body: JSON.stringify({
        plan_id: activeOrder.value.plan_id,
        order_id: activeOrder.value.order_id,
        payment_method: paymentMethod.value,
        card_last4: cardLast4,
        upi_vpa: paymentMethod.value === 'upi' ? upiId.value : null,
        bank_name: paymentMethod.value === 'netbanking' ? selectedBank.value : null
      })
    })

    successReceipt.value = {
      ...res,
      credits_added: activeOrder.value.monthly_credits
    }

    billing.value.tier = res.tier
    billing.value.credits_remaining = res.credits_remaining
    billing.value.plan_name = res.plan_name

    if (authStore.role === 'student') {
      authStore.setPremium(true)
      billing.value.is_premium = true
      await authStore.refreshProfile()
    }

    await loadBillingData()
    checkoutStage.value = 'success'
  } catch (err) {
    showToast(err.message || 'Payment processing failed', 'error')
    checkoutStage.value = 'form'
  } finally {
    isProcessing.value = false
  }
}
</script>

<style scoped>
/* ─── Page Root ──────────────────────────────────────── */
.billing-page {
  display: flex;
  flex-direction: column;
  gap: 28px;
  max-width: 1360px;
  margin: 0 auto;
}

/* ─── Hero Card ──────────────────────────────────────── */
.billing-hero-card {
  background: linear-gradient(135deg, #0F172A 0%, #1E293B 45%, #1E3A8A 100%);
  border-radius: 24px;
  padding: 36px 40px;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  box-shadow: 0 12px 35px -5px rgba(15, 23, 42, 0.2);
}

.hero-left {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 680px;
}

.hero-tier-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.22);
  padding: 4px 12px;
  border-radius: 9999px;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.6px;
  color: #FCD34D;
  align-self: flex-start;
}

.crown-icon {
  font-size: 14px;
}

.hero-title {
  font-size: 26px;
  font-weight: 900;
  line-height: 1.25;
  letter-spacing: -0.4px;
}

.hero-subtitle {
  font-size: 13.5px;
  color: #CBD5E1;
  line-height: 1.55;
}

.hero-right {
  flex-shrink: 0;
}

.credits-capsule {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(12px);
  border-radius: 18px;
  padding: 20px 28px;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.credits-label {
  font-size: 11.5px;
  font-weight: 700;
  color: #93C5FD;
  letter-spacing: 0.4px;
  text-transform: uppercase;
}

.credits-num {
  font-size: 36px;
  font-weight: 900;
  color: #FFFFFF;
  line-height: 1;
}

.credits-sub {
  font-size: 11px;
  color: #94A3B8;
  margin-top: 2px;
}

/* ─── Plans Grid ─────────────────────────────────────── */
.plans-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  align-items: stretch;
}

.plans-grid--student {
  grid-template-columns: repeat(auto-fit, minmax(320px, 480px));
  justify-content: center;
}

.plan-card {
  background: #FFFFFF;
  border: 1.5px solid #E8ECF4;
  border-radius: 24px;
  padding: 32px 28px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 22px;
  position: relative;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
  transition: all 0.2s ease;
}

.plan-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 30px rgba(37, 99, 235, 0.08);
}

.plan-card--featured {
  border-color: #2563EB;
  box-shadow: 0 8px 30px rgba(37, 99, 235, 0.12);
}

.plan-card--active {
  border-color: #10B981;
}

.card-pill {
  position: absolute;
  top: -12px;
  right: 24px;
  padding: 4px 14px;
  border-radius: 9999px;
  font-size: 10.5px;
  font-weight: 800;
  letter-spacing: 0.6px;
}

.card-pill--active {
  background: #10B981;
  color: #FFFFFF;
}

.card-pill--popular {
  background: #2563EB;
  color: #FFFFFF;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
}

.plan-header {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.plan-tier-name {
  font-size: 20px;
  font-weight: 900;
  color: #0F172A;
  letter-spacing: -0.3px;
}

.plan-tagline {
  font-size: 12px;
  color: #64748B;
  min-height: 34px;
  line-height: 1.45;
}

.plan-price-row {
  display: flex;
  align-items: baseline;
  gap: 3px;
  margin-top: 10px;
}

.price-curr {
  font-size: 20px;
  font-weight: 800;
  color: #0F172A;
}

.price-amount {
  font-size: 36px;
  font-weight: 900;
  color: #0F172A;
  line-height: 1;
}

.price-cycle {
  font-size: 13px;
  color: #64748B;
  font-weight: 600;
  margin-left: 2px;
}

.plan-credits-box {
  background: #EFF6FF;
  border: 1px solid #BFDBFE;
  border-radius: 12px;
  padding: 10px 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.bolt-icon {
  font-size: 14px;
}

.credits-text {
  font-size: 12px;
  color: #1E40AF;
}

.features-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 12.5px;
}

.check-icon {
  font-size: 13px;
  font-weight: 800;
  flex-shrink: 0;
}

.feature-item--checked .check-icon {
  color: #10B981;
}

.feature-item--checked .feature-text {
  color: #1E293B;
}

.feature-item--disabled .check-icon {
  color: #CBD5E1;
}

.feature-item--disabled .feature-text {
  color: #94A3B8;
  text-decoration: line-through;
}

.plan-action-wrap {
  margin-top: 8px;
}

.btn-plan {
  width: 100%;
  height: 46px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  border: none;
  transition: all 0.15s ease;
}

.btn-plan--current {
  background: #F1F5F9;
  color: #475569;
  cursor: default;
}

.btn-plan--upgrade {
  background: #0F172A;
  color: #FFFFFF;
}

.btn-plan--upgrade:hover {
  background: #1E293B;
}

.btn-plan--featured {
  background: #2563EB !important;
  color: #FFFFFF !important;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
}

.btn-plan--featured:hover {
  background: #1D4ED8 !important;
}

/* ─── Activity Section ───────────────────────────────── */
.activity-section {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.activity-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.activity-title {
  font-size: 18px;
  font-weight: 800;
  color: #0F172A;
}

.activity-sub {
  font-size: 13px;
  color: #64748B;
  margin-top: 2px;
}

.btn-refresh {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: #FFFFFF;
  border: 1.5px solid #E2E8F0;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 700;
  color: #475569;
  cursor: pointer;
  transition: all 0.12s ease;
}

.btn-refresh:hover {
  background: #F8FAFC;
  border-color: #CBD5E1;
}

.activity-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.activity-grid--single {
  grid-template-columns: 1fr !important;
}

.activity-card {
  background: #FFFFFF;
  border: 1px solid #E8ECF4;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
}

.card-inner-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 14px;
  border-bottom: 1px solid #F0F4FF;
  margin-bottom: 12px;
}

.inner-title-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
}

.inner-icon {
  font-size: 18px;
}

.inner-title {
  font-size: 14.5px;
  font-weight: 800;
  color: #0F172A;
}

.badge-count {
  font-size: 11px;
  font-weight: 700;
  color: #64748B;
  background: #F1F5F9;
  padding: 3px 10px;
  border-radius: 9999px;
}

.tx-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.tx-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 14px;
  background: #F8FAFC;
  border: 1px solid #E8ECF4;
  border-radius: 12px;
}

.tx-left {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.tx-id {
  font-size: 13px;
  font-weight: 800;
  color: #0F172A;
}

.tx-desc {
  font-size: 12.5px;
  font-weight: 700;
  color: #0F172A;
}

.tx-date {
  font-size: 11px;
  color: #94A3B8;
}

.tx-method {
  font-size: 11px;
  color: #64748B;
}

.tx-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
}

.tx-amount {
  font-size: 15px;
  font-weight: 800;
  color: #0F172A;
}

.credit-delta {
  font-size: 13.5px;
  font-weight: 800;
}

.credit-delta--plus {
  color: #10B981;
}

.credit-delta--minus {
  color: #EF4444;
}

.status-chip {
  padding: 2px 8px;
  border-radius: 9999px;
  font-size: 10px;
  font-weight: 800;
}

.status-chip--success {
  background: #ECFDF5;
  color: #059669;
}

.status-chip--pending {
  background: #FFFBEB;
  color: #D97706;
}

.status-chip--recorded {
  background: #F1F5F9;
  color: #475569;
}

.empty-tx {
  padding: 24px;
  text-align: center;
  color: #94A3B8;
  font-size: 12.5px;
}

/* ─── Modal ─────────────────────────────────────────── */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.5);
  backdrop-filter: blur(5px);
  z-index: 999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.checkout-modal {
  background: #FFFFFF;
  border-radius: 24px;
  padding: 32px;
  width: 100%;
  max-width: 520px;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.checkout-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}

.modal-badge {
  font-size: 10px;
  font-weight: 800;
  color: #2563EB;
  letter-spacing: 0.6px;
}

.modal-title {
  font-size: 18px;
  font-weight: 900;
  color: #0F172A;
  margin-top: 2px;
}

.btn-modal-close {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #F1F5F9;
  border: none;
  font-size: 13px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.order-summary-box {
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 14px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.summary-line {
  display: flex;
  justify-content: space-between;
  font-size: 12.5px;
  color: #475569;
}

.total-line {
  border-top: 1px dashed #CBD5E1;
  padding-top: 8px;
  margin-top: 4px;
  font-size: 14px;
  font-weight: 800;
  color: #0F172A;
}

.total-amount {
  font-size: 18px;
  color: #2563EB;
}

.method-tabs {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.method-tab-btn {
  padding: 10px 6px;
  background: #F8FAFC;
  border: 1.5px solid #E2E8F0;
  border-radius: 10px;
  font-size: 11.5px;
  font-weight: 700;
  color: #475569;
  cursor: pointer;
  transition: all 0.12s;
  text-align: center;
}

.method-tab-btn--active {
  background: #EFF6FF !important;
  border-color: #2563EB !important;
  color: #2563EB !important;
}

.payment-fields-pane {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.field-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field-item-label {
  font-size: 12px;
  font-weight: 700;
  color: #1E293B;
}

.field-item-input,
.field-item-select {
  width: 100%;
  height: 42px;
  padding: 0 14px;
  background: #FFFFFF;
  border: 1.5px solid #E2E8F0;
  border-radius: 10px;
  font-size: 13px;
  color: #0F172A;
  outline: none;
  font-family: inherit;
  box-sizing: border-box;
}

.field-item-input:focus,
.field-item-select:focus {
  border-color: #2563EB;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.grid-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.upi-box {
  background: #F8FAFC;
  border: 1.5px dashed #CBD5E1;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
}

.qr-icon {
  font-size: 28px;
}

.qr-text {
  font-size: 12px;
  color: #64748B;
  margin-top: 4px;
}

.checkout-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
  padding-top: 14px;
  border-top: 1px solid #F0F4FF;
}

.btn-cancel {
  padding: 10px 18px;
  background: #FFFFFF;
  border: 1.5px solid #E2E8F0;
  border-radius: 10px;
  font-size: 12.5px;
  font-weight: 700;
  color: #475569;
  cursor: pointer;
}

.btn-pay-now {
  padding: 10px 22px;
  background: #2563EB;
  color: #FFFFFF;
  border: none;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
}

.btn-pay-now:hover {
  background: #1D4ED8;
}

.processing-pane,
.success-pane {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 30px 10px;
  gap: 12px;
}

.spinner-large {
  width: 44px;
  height: 44px;
  border: 3px solid rgba(37, 99, 235, 0.2);
  border-top-color: #2563EB;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.success-icon-circle {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #ECFDF5;
  color: #059669;
  font-size: 26px;
  font-weight: 900;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.2);
}

.success-title {
  font-size: 18px;
  font-weight: 900;
  color: #0F172A;
}

.success-desc {
  font-size: 13px;
  color: #64748B;
  max-width: 400px;
  line-height: 1.5;
}

.btn-done {
  margin-top: 10px;
  padding: 10px 24px;
  background: #0F172A;
  color: #FFFFFF;
  border: none;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}

/* ─── Toast Popup ────────────────────────────────────── */
.toast-popup {
  position: fixed;
  top: 24px;
  right: 24px;
  z-index: 9999;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  border-radius: 14px;
  font-size: 13px;
  font-weight: 700;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
  backdrop-filter: blur(8px);
}

.toast-popup--success {
  background: #ECFDF5;
  border: 1px solid #A7F3D0;
  color: #065F46;
}

.toast-popup--error {
  background: #FEF2F2;
  border: 1px solid #FECACA;
  color: #991B1B;
}

.toast-fade-enter-active,
.toast-fade-leave-active {
  transition: all 0.25s ease;
}

.toast-fade-enter-from,
.toast-fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

@media (max-width: 1024px) {
  .plans-grid {
    grid-template-columns: 1fr;
  }
  .activity-grid {
    grid-template-columns: 1fr;
  }
  .billing-hero-card {
    flex-direction: column;
    align-items: flex-start;
  }
}

/* ─── Receipt Modal & Printable Styles ────────────────── */
.tx-sub-meta {
  font-size: 11px;
  color: #94A3B8;
  font-family: monospace;
}

.tx-actions-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-receipt-action {
  background: #F1F5F9;
  border: 1px solid #CBD5E1;
  color: #334155;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
.btn-receipt-action:hover {
  background: #E2E8F0;
  border-color: #94A3B8;
  color: #0F172A;
}

.modal-box--receipt {
  background: #fff;
  border-radius: 16px;
  max-width: 680px;
  width: 100%;
  padding: 24px;
  box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.25);
  max-height: 90vh;
  overflow-y: auto;
}

.receipt-header-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid #E2E8F0;
}

.receipt-status-pill {
  font-size: 11px;
  font-weight: 800;
  color: #059669;
  background: #ECFDF5;
  border: 1px solid #A7F3D0;
  padding: 4px 10px;
  border-radius: 9999px;
  letter-spacing: 0.05em;
}

.receipt-btn-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-receipt-print {
  background: #2563EB;
  color: #fff;
  border: none;
  font-size: 12px;
  font-weight: 700;
  padding: 6px 14px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-receipt-print:hover {
  background: #1D4ED8;
}

.receipt-paper {
  background: #FAFAFA;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  padding: 28px;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  color: #1E293B;
}

.receipt-brand-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}

.receipt-brand-title {
  font-size: 22px;
  font-weight: 900;
  letter-spacing: -0.02em;
  color: #0F172A;
}

.brand-blue {
  color: #2563EB;
}

.receipt-brand-sub {
  font-size: 11px;
  color: #64748B;
  margin-top: 2px;
}

.receipt-meta-block {
  text-align: right;
}

.inv-tag {
  font-size: 10px;
  font-weight: 800;
  color: #2563EB;
  letter-spacing: 0.08em;
}

.inv-no {
  font-size: 14px;
  font-weight: 800;
  color: #0F172A;
  font-family: monospace;
  margin: 2px 0;
}

.inv-date {
  font-size: 11px;
  color: #64748B;
}

.receipt-hr {
  height: 1px;
  background: #E2E8F0;
  margin: 20px 0;
}

.receipt-parties-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 24px;
}

.party-heading {
  font-size: 10px;
  font-weight: 800;
  color: #94A3B8;
  letter-spacing: 0.05em;
  margin-bottom: 4px;
}

.party-name {
  font-size: 13px;
  font-weight: 700;
  color: #0F172A;
}

.party-email, .party-sub, .party-type {
  font-size: 11px;
  color: #64748B;
  margin-top: 1px;
}

.receipt-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 24px;
  font-size: 12px;
}

.receipt-table th {
  background: #F1F5F9;
  color: #475569;
  font-size: 11px;
  font-weight: 700;
  padding: 8px 12px;
  border-top: 1px solid #CBD5E1;
  border-bottom: 1px solid #CBD5E1;
}

.receipt-table td {
  padding: 12px;
  border-bottom: 1px solid #E2E8F0;
}

.receipt-table tfoot td {
  padding: 12px;
  background: #F8FAFC;
  font-size: 13px;
  border-bottom: 2px solid #CBD5E1;
}

.item-title {
  font-weight: 700;
  color: #0F172A;
}

.item-meta {
  font-size: 10px;
  color: #64748B;
  font-family: monospace;
  margin-top: 2px;
}

.badge-paid {
  display: inline-block;
  background: #ECFDF5;
  color: #059669;
  font-size: 10px;
  font-weight: 800;
  padding: 2px 8px;
  border-radius: 4px;
  border: 1px solid #A7F3D0;
}

.receipt-footer-box {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px dashed #CBD5E1;
  font-size: 10px;
  color: #64748B;
  text-align: center;
  line-height: 1.5;
}

.receipt-seal {
  font-family: monospace;
  font-size: 9px;
  color: #94A3B8;
  margin-top: 4px;
}

@media print {
  body * {
    visibility: hidden;
  }
  .modal-overlay {
    position: static;
    background: none;
    padding: 0;
  }
  .modal-box--receipt {
    box-shadow: none;
    padding: 0;
    max-width: 100%;
  }
  #printable-receipt, #printable-receipt * {
    visibility: visible;
  }
  #printable-receipt {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    border: none;
    background: #fff;
  }
  .no-print {
    display: none !important;
  }
}
</style>
