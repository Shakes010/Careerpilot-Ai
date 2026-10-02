import uuid
import json
from datetime import datetime, timezone
from passlib.context import CryptContext
from app.database import engine, Base, SessionLocal
import app.models as models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_database():
    print("Creating all database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

    db = SessionLocal()
    try:
        # 1. Seed Admin User
        admin_user = db.query(models.User).filter(models.User.email == "admin@careerpilot.ai").first()
        if not admin_user:
            admin_user = models.User(
                email="admin@careerpilot.ai",
                password_hash=pwd_context.hash("admin123"),
                role=models.UserRole.admin,
                full_name="CareerPilot System Admin",
                is_verified=True,
                is_active=True
            )
            db.add(admin_user)
            db.commit()

        # 2. Seed Skills
        default_skills = [
            ("Python", "Backend"),
            ("FastAPI", "Backend"),
            ("SQLAlchemy", "Backend"),
            ("PostgreSQL", "Database"),
            ("SQL", "Database"),
            ("JavaScript", "Frontend"),
            ("Vue.js", "Frontend"),
            ("TypeScript", "Frontend"),
            ("Node.js", "Backend"),
            ("Machine Learning", "AI/ML"),
            ("Data Structures & Algorithms", "Core CS"),
            ("System Design", "Core CS"),
            ("Git", "DevOps"),
            ("Docker", "DevOps"),
            ("React", "Frontend")
        ]

        for s_name, cat in default_skills:
            existing = db.query(models.Skill).filter(models.Skill.skill_name == s_name).first()
            if not existing:
                db.add(models.Skill(skill_name=s_name, category=cat))
        db.commit()

        # 3. Seed Subscription Plans
        default_plans = [
            ("Free Tier Plan", models.PlanTier.free, 10, 0.0, ["candidate_search", "shortlisting"]),
            ("Basic Recruiter Plan", models.PlanTier.basic, 50, 1999.0, ["candidate_search", "shortlisting", "candidate_comparison"]),
            ("Premium Recruiter Plan", models.PlanTier.premium, 200, 4999.0, ["candidate_search", "shortlisting", "candidate_comparison", "match_explainability", "recruiter_analytics"])
        ]

        for name, tier, credits, price, feats in default_plans:
            existing = db.query(models.Plan).filter(models.Plan.tier == tier).first()
            if not existing:
                db.add(models.Plan(
                    plan_name=name,
                    tier=tier,
                    monthly_credits=credits,
                    price_inr=price,
                    features=feats
                ))
        db.commit()

        # 4. Seed Career Sandbox Challenges
        python_skill = db.query(models.Skill).filter(models.Skill.skill_name == "Python").first()
        fastapi_skill = db.query(models.Skill).filter(models.Skill.skill_name == "FastAPI").first()

        sandbox_challenges = [
            ("FastAPI RESTful Endpoint Challenge", "Implement a GET and POST endpoint with Pydantic validation.", fastapi_skill.id if fastapi_skill else None, "Medium"),
            ("Python Data Processing Pipeline", "Parse JSON payloads and calculate aggregate statistics.", python_skill.id if python_skill else None, "Easy")
        ]

        for title, desc, s_id, diff in sandbox_challenges:
            existing = db.query(models.CareerSandboxChallenge).filter(models.CareerSandboxChallenge.title == title).first()
            if not existing:
                db.add(models.CareerSandboxChallenge(
                    title=title,
                    description=desc,
                    skill_id=s_id,
                    difficulty=diff
                ))
        db.commit()

        # 5. Seed 3 Variants for Core Skills (Fixed Language: is_language_flexible = False)
        skill_variants = [
            ("Python", [
                ("Python Core Verification (Variant 1: Fundamentals)", [
                    (1, "Checkpoint 1: Functions & Control Flow", "Write a function `reverse_words(sentence: str) -> str`.", "def reverse_words(sentence: str):\n    return ' '.join(sentence.split()[::-1])"),
                    (2, "Checkpoint 2: Dictionary Operations", "Write a function `word_frequencies(text: str) -> dict`.", "def word_frequencies(text: str):\n    counts = {}\n    for w in text.split():\n        counts[w] = counts.get(w, 0) + 1\n    return counts"),
                    (3, "Checkpoint 3: Algorithmic Efficiency", "Implement an efficient `find_duplicates(nums: list) -> list`.", "def find_duplicates(nums: list):\n    seen = set()\n    dups = set()\n    for x in nums:\n        if x in seen:\n            dups.add(x)\n        seen.add(x)\n    return list(dups)")
                ]),
                ("Python Core Verification (Variant 2: Data Structures)", [
                    (1, "Checkpoint 1: List Comprehension & Filter", "Write a function `filter_evens(nums: list) -> list`.", "def filter_evens(nums: list):\n    return [x for x in nums if x % 2 == 0]"),
                    (2, "Checkpoint 2: Matrix Rotation", "Write a function `rotate_matrix(matrix: list) -> list`.", "def rotate_matrix(matrix: list):\n    return [list(row) for row in zip(*matrix[::-1])]"),
                    (3, "Checkpoint 3: LRU Cache Helper", "Implement a cache eviction helper `evict_lru(cache: dict, key: str)`.", "def evict_lru(cache: dict, key: str):\n    if key in cache:\n        cache.pop(key)\n    return cache")
                ]),
                ("Python Core Verification (Variant 3: OOP & Logic)", [
                    (1, "Checkpoint 1: Class Definition & Inheritance", "Define a `BankAccount` class with `deposit` and `withdraw` methods.", "class BankAccount:\n    def __init__(self, balance=0):\n        self.balance = balance\n    def deposit(self, amt):\n        self.balance += amt\n    def withdraw(self, amt):\n        if amt <= self.balance: self.balance -= amt"),
                    (2, "Checkpoint 2: Custom Exception Handling", "Implement a custom exception `InsufficientFundsError`.", "class InsufficientFundsError(Exception): pass"),
                    (3, "Checkpoint 3: Generator Yield Loop", "Write a generator `fibonacci(n: int)` yielding sequence items.", "def fibonacci(n: int):\n    a, b = 0, 1\n    for _ in range(n):\n        yield a\n        a, b = b, a + b")
                ])
            ]),
            ("SQL", [
                ("SQL Database Verification (Variant 1: Basic Queries)", [
                    (1, "Checkpoint 1: SELECT & Filtering", "Write SQL SELECT query filtering active students.", "SELECT * FROM students WHERE is_active = true;"),
                    (2, "Checkpoint 2: GROUP BY Aggregation", "Write SQL query counting students by department.", "SELECT department, COUNT(*) FROM students GROUP BY department;"),
                    (3, "Checkpoint 3: INNER JOIN Queries", "Write query joining students and enrollments tables.", "SELECT s.name, e.course FROM students s JOIN enrollments e ON s.id = e.student_id;")
                ]),
                ("SQL Database Verification (Variant 2: Advanced Joins)", [
                    (1, "Checkpoint 1: LEFT OUTER JOIN", "Select all companies and their posted job titles.", "SELECT c.name, j.title FROM companies c LEFT JOIN jobs j ON c.id = j.company_id;"),
                    (2, "Checkpoint 2: Subqueries IN Clause", "Find students with GPA above average.", "SELECT name FROM students WHERE gpa > (SELECT AVG(gpa) FROM students);"),
                    (3, "Checkpoint 3: HAVING Filter", "Find departments with more than 5 students.", "SELECT department, COUNT(*) FROM students GROUP BY department HAVING COUNT(*) > 5;")
                ]),
                ("SQL Database Verification (Variant 3: Window Functions)", [
                    (1, "Checkpoint 1: ROW_NUMBER Partition", "Write query ranking salaries by department.", "SELECT name, salary, ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) FROM employees;"),
                    (2, "Checkpoint 2: DENSE_RANK Aggregations", "Calculate dense rank for candidate trust scores.", "SELECT user_id, DENSE_RANK() OVER (ORDER BY trust_score DESC) FROM student_skills;"),
                    (3, "Checkpoint 3: CTE Expressions", "Use WITH statement to filter top candidates.", "WITH TopCands AS (SELECT * FROM student_skills WHERE trust_score >= 80) SELECT * FROM TopCands;")
                ])
            ]),
            ("FastAPI", [
                ("FastAPI REST API Verification (Variant 1: Endpoints)", [
                    (1, "Checkpoint 1: Path & Query Parameters", "Define GET `/items/{item_id}` endpoint returning item details.", "@app.get('/items/{item_id}')\ndef get_item(item_id: int, q: str = None):\n    return {'item_id': item_id, 'q': q}"),
                    (2, "Checkpoint 2: Pydantic Model Validation", "Define Pydantic `ItemCreate` schema.", "from pydantic import BaseModel\nclass ItemCreate(BaseModel):\n    name: str\n    price: float"),
                    (3, "Checkpoint 3: POST Body Handling", "Create POST `/items/` endpoint accepting Pydantic body.", "@app.post('/items/')\ndef create_item(item: ItemCreate):\n    return {'name': item.name, 'price': item.price}")
                ]),
                ("FastAPI REST API Verification (Variant 2: Middleware & Auth)", [
                    (1, "Checkpoint 1: OAuth2 Bearer Header", "Set up OAuth2PasswordBearer dependency.", "from fastapi.security import OAuth2PasswordBearer\noauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')"),
                    (2, "Checkpoint 2: CORS Middleware Setup", "Add CORSMiddleware to FastAPI app.", "app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'])"),
                    (3, "Checkpoint 3: Custom Exception Handlers", "Create HTTP Exception handler for 404.", "raise HTTPException(status_code=404, detail='Item not found')")
                ]),
                ("FastAPI REST API Verification (Variant 3: Async & DB)", [
                    (1, "Checkpoint 1: Async Def Router", "Write async GET endpoint for health check.", "@app.get('/health')\nasync def health():\n    return {'status': 'ok'}"),
                    (2, "Checkpoint 2: SQLAlchemy Session Dependency", "Create `get_db` generator dependency.", "def get_db():\n    db = SessionLocal()\n    try:\n        yield db\n    finally:\n        db.close()"),
                    (3, "Checkpoint 3: Async Task Handling", "Write background task function for email notifications.", "from fastapi import BackgroundTasks\ndef send_email(email: str):\n    pass")
                ])
            ]),
            ("Vue.js", [
                ("Vue.js Frontend Verification (Variant 1: Reactivity)", [
                    (1, "Checkpoint 1: ref & reactive State", "Declare reactive counter ref in Composition API.", "import { ref } from 'vue'\nconst count = ref(0)"),
                    (2, "Checkpoint 2: computed Property", "Create computed property `doubleCount`.", "import { computed } from 'vue'\nconst doubleCount = computed(() => count.value * 2)"),
                    (3, "Checkpoint 3: Event Handlers & v-model", "Bind text input to `searchQuery` ref.", "<input v-model='searchQuery' />")
                ]),
                ("Vue.js Frontend Verification (Variant 2: Pinia Store)", [
                    (1, "Checkpoint 1: defineStore Setup", "Create Pinia `useUserStore` with state.", "export const useUserStore = defineStore('user', { state: () => ({ user: null }) })"),
                    (2, "Checkpoint 2: Action Dispatcher", "Add `loginUser` action to Pinia store.", "actions: { loginUser(data) { this.user = data } }"),
                    (3, "Checkpoint 3: Getter Helper", "Add getter `isLoggedIn` to Pinia store.", "getters: { isLoggedIn: (state) => !!state.user }")
                ]),
                ("Vue.js Frontend Verification (Variant 3: Vue Router)", [
                    (1, "Checkpoint 1: Route Definitions", "Define routes array with login and dashboard.", "const routes = [{ path: '/', component: Dashboard }]"),
                    (2, "Checkpoint 2: Navigation Guards", "Create `beforeEach` navigation guard for auth.", "router.beforeEach((to, from, next) => { next() })"),
                    (3, "Checkpoint 3: Dynamic Route Params", "Access route parameter `useRoute().params.id`.", "import { useRoute } from 'vue-router'\nconst route = useRoute()")
                ])
            ]),
            ("JavaScript", [
                ("JavaScript ES6+ Verification (Variant 1: Array Ops)", [
                    (1, "Checkpoint 1: Array Map & Filter", "Filter even numbers and square them.", "const result = nums.filter(x => x % 2 === 0).map(x => x * x);"),
                    (2, "Checkpoint 2: Array Reduce Aggregation", "Calculate sum of numbers array.", "const sum = nums.reduce((acc, curr) => acc + curr, 0);"),
                    (3, "Checkpoint 3: Object Destructuring", "Destructure `name` and `email` from user object.", "const { name, email } = user;")
                ]),
                ("JavaScript ES6+ Verification (Variant 2: Async/Await)", [
                    (1, "Checkpoint 1: Fetch API Call", "Fetch JSON data from endpoint using async/await.", "async function getData() {\n  const res = await fetch('/api/data');\n  return res.json();\n}"),
                    (2, "Checkpoint 2: Promise.all Concurrent Execution", "Execute multiple promises concurrently.", "const [user, posts] = await Promise.all([fetchUser(), fetchPosts()]);"),
                    (3, "Checkpoint 3: Try/Catch Async Errors", "Handle fetch errors with try/catch block.", "try { await getData(); } catch (err) { console.error(err); }")
                ]),
                ("JavaScript ES6+ Verification (Variant 3: Closures & Scope)", [
                    (1, "Checkpoint 1: Closure Function", "Create a counter function using closure.", "function createCounter() {\n  let count = 0;\n  return () => ++count;\n}"),
                    (2, "Checkpoint 2: Arrow Function Binding", "Use arrow function to retain `this` context.", "const obj = { name: 'App', getName: () => this.name };"),
                    (3, "Checkpoint 3: Template Literals & Modules", "Format string using template literal.", "const msg = `Hello ${name}, welcome back!`;")
                ])
            ])
        ]

        for skill_name, variants in skill_variants:
            sk = db.query(models.Skill).filter(models.Skill.skill_name == skill_name).first()
            if sk:
                for ass_title, checkpoints in variants:
                    existing_ass = db.query(models.Assessment).filter(models.Assessment.assessment_name == ass_title).first()
                    if not existing_ass:
                        ass = models.Assessment(
                            assessment_name=ass_title,
                            assessment_type=models.AssessmentType.programming,
                            skill_id=sk.id,
                            is_language_flexible=False
                        )
                        db.add(ass)
                        db.flush()

                        for seq, cp_title, inst, val in checkpoints:
                            db.add(models.AssessmentCheckpoint(
                                assessment_id=ass.id,
                                sequence_order=seq,
                                title=cp_title,
                                instructions=inst,
                                validation_test=val
                            ))
                        db.commit()

        # 6. Seed 3 General / Aptitude Assessments (Language Flexible: is_language_flexible = True, skill_id = None)
        general_assessments = [
            ("General Programming Logic: Range Loop & Multiples", [
                (1, "Checkpoint 1: Loop Counter", "Write code that reads integer `N` from stdin and prints numbers from 0 to N-1 separated by spaces.", json.dumps([{"input": "5", "expected_output": "0 1 2 3 4"}, {"input": "3", "expected_output": "0 1 2"}])),
                (2, "Checkpoint 2: Multiples Filter", "Write code that reads `N` and prints all multiples of 3 or 5 up to N.", json.dumps([{"input": "15", "expected_output": "3 5 6 9 10 12 15"}, {"input": "10", "expected_output": "3 5 6 9 10"}])),
                (3, "Checkpoint 3: Multiples Sum Result", "Write code that calculates the sum of all multiples of 3 or 5 up to N.", json.dumps([{"input": "10", "expected_output": "33"}, {"input": "15", "expected_output": "60"}]))
            ]),
            ("Algorithmic Fundamentals: String Processing & Palindromes", [
                (1, "Checkpoint 1: String Reversal", "Write code that reads string input and prints the string reversed.", json.dumps([{"input": "hello", "expected_output": "olleh"}, {"input": "pilot", "expected_output": "tolip"}])),
                (2, "Checkpoint 2: Vowel Count", "Write code that counts total vowels (a, e, i, o, u) in input string.", json.dumps([{"input": "careerpilot", "expected_output": "5"}, {"input": "algorithm", "expected_output": "3"}])),
                (3, "Checkpoint 3: Palindrome Check", "Write code that checks if input string is a palindrome (prints True or False).", json.dumps([{"input": "racecar", "expected_output": "True"}, {"input": "hello", "expected_output": "False"}]))
            ]),
            ("Problem Solving: Array Target Find & Max", [
                (1, "Checkpoint 1: Max Element Find", "Write code that reads space-separated integers and prints the maximum number.", json.dumps([{"input": "3 1 9 4 5", "expected_output": "9"}, {"input": "12 45 7 89 23", "expected_output": "89"}])),
                (2, "Checkpoint 2: Array Sum Calculation", "Write code that reads space-separated integers and prints their total sum.", json.dumps([{"input": "10 20 30", "expected_output": "60"}, {"input": "5 5 5 5", "expected_output": "20"}])),
                (3, "Checkpoint 3: Target Search", "Write code that reads space-separated numbers and checks if target 10 exists (prints Found or Not Found).", json.dumps([{"input": "2 4 10 8", "expected_output": "Found"}, {"input": "1 3 5 7", "expected_output": "Not Found"}]))
            ])
        ]

        for ass_title, cps in general_assessments:
            existing_ass = db.query(models.Assessment).filter(models.Assessment.assessment_name == ass_title).first()
            if not existing_ass:
                ass = models.Assessment(
                    assessment_name=ass_title,
                    assessment_type=models.AssessmentType.aptitude,
                    skill_id=None,
                    is_language_flexible=True
                )
                db.add(ass)
                db.flush()

                for seq, cp_title, inst, val_json in cps:
                    db.add(models.AssessmentCheckpoint(
                        assessment_id=ass.id,
                        sequence_order=seq,
                        title=cp_title,
                        instructions=inst,
                        validation_test=val_json
                    ))
                db.commit()

        print("Database seed completed successfully.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
