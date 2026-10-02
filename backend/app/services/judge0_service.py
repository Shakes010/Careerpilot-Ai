"""
Judge0 CE Integration Service
Handles code execution via the Judge0 CE RapidAPI endpoint.
Docs: https://ce.judge0.com/
"""
import base64
import time
import requests
from typing import List, Optional
from app.config import settings

# Judge0 CE language IDs (most relevant subset)
LANGUAGE_IDS = {
    "python": 71,       # Python 3.8.1
    "javascript": 63,   # JavaScript (Node.js 12.14.0)
    "java": 62,         # Java (OpenJDK 13.0.1)
    "cpp": 54,          # C++ (GCC 9.2.0)
    "c": 50,            # C (GCC 9.2.0)
    "typescript": 74,   # TypeScript (3.7.4)
    "sql": 82,          # SQL (SQLite 3.27.2)
}

JUDGE0_BASE_URL = f"https://{settings.JUDGE0_API_HOST}"


def _encode(text: str) -> str:
    """Base64-encode a string for Judge0's base64_encoded mode."""
    return base64.b64encode(text.encode()).decode()


def _decode(text: Optional[str]) -> str:
    """Base64-decode a Judge0 response field."""
    if not text:
        return ""
    try:
        return base64.b64decode(text).decode("utf-8", errors="replace")
    except Exception:
        return text


def _get_headers() -> dict:
    return {
        "x-rapidapi-key": settings.JUDGE0_API_KEY,
        "x-rapidapi-host": settings.JUDGE0_API_HOST,
        "Content-Type": "application/json",
    }


def run_code(source_code: str, language_id: int, stdin: str = "") -> dict:
    """
    Submit code to Judge0 and poll for result.
    Returns dict with keys: stdout, stderr, compile_output, status_id, status_desc, time, memory
    """
    if not settings.JUDGE0_API_KEY:
        # Graceful fallback when no key is configured (dev/demo mode)
        return _mock_run(source_code, stdin)

    payload = {
        "source_code": _encode(source_code),
        "language_id": language_id,
        "stdin": _encode(stdin),
        "base64_encoded": True,
        "wait": False,
    }

    try:
        # Submit
        resp = requests.post(
            f"{JUDGE0_BASE_URL}/submissions",
            json=payload,
            headers=_get_headers(),
            timeout=15,
            params={"base64_encoded": "true", "wait": "false"},
        )
        resp.raise_for_status()
        token = resp.json().get("token")
        if not token:
            return _error_result("No token returned from Judge0")

        # Poll for result (max 10 seconds)
        for _ in range(20):
            time.sleep(0.5)
            poll = requests.get(
                f"{JUDGE0_BASE_URL}/submissions/{token}",
                headers=_get_headers(),
                params={"base64_encoded": "true"},
                timeout=10,
            )
            poll.raise_for_status()
            data = poll.json()
            status_id = data.get("status", {}).get("id", 0)
            # status_id 1=In Queue, 2=Processing — keep polling
            if status_id not in (1, 2):
                return {
                    "stdout": _decode(data.get("stdout")),
                    "stderr": _decode(data.get("stderr")),
                    "compile_output": _decode(data.get("compile_output")),
                    "status_id": status_id,
                    "status_desc": data.get("status", {}).get("description", "Unknown"),
                    "time": data.get("time"),
                    "memory": data.get("memory"),
                }

        return _error_result("Judge0 timeout — execution took too long")

    except requests.RequestException as e:
        return _error_result(f"Judge0 request failed: {str(e)}")


def _error_result(msg: str) -> dict:
    return {
        "stdout": "",
        "stderr": msg,
        "compile_output": "",
        "status_id": -1,
        "status_desc": "Internal Error",
        "time": None,
        "memory": None,
    }


def _mock_run(source_code: str, stdin: str) -> dict:
    """
    Mock execution used when JUDGE0_API_KEY is not set.
    Attempts a basic Python syntax check only — not a real runner.
    Returns a fake 'Accepted' for non-empty code.
    """
    if not source_code.strip():
        return {
            "stdout": "",
            "stderr": "No code submitted.",
            "compile_output": "",
            "status_id": 6,  # Compilation Error
            "status_desc": "Compilation Error",
            "time": None,
            "memory": None,
        }
    # Fake acceptance (mock mode)
    return {
        "stdout": "__MOCK__",
        "stderr": "",
        "compile_output": "",
        "status_id": 3,  # Accepted
        "status_desc": "Accepted (Mock)",
        "time": "0.1",
        "memory": 1024,
    }


def evaluate_checkpoint(
    submitted_code: str,
    language_id: int,
    test_cases: List[dict],
) -> dict:
    """
    Run submitted_code against every test case and return pass/fail per case.

    test_cases: [{"input": "...", "expected_output": "..."}]

    Returns:
    {
        "passed": bool,               # True only if ALL test cases pass
        "total": int,
        "passed_count": int,
        "results": [
            {
                "index": int,          # 1-indexed for display
                "passed": bool,
                "error": str | None,   # runtime/compile error message (no expected_output leak)
            }
        ]
    }
    """
    results = []
    passed_count = 0

    for i, tc in enumerate(test_cases):
        expected = (tc.get("expected_output") or "").strip()
        stdin = tc.get("input") or ""

        run_result = run_code(submitted_code, language_id, stdin)

        status_id = run_result["status_id"]
        actual_stdout = run_result["stdout"].strip()

        # status_id 3 = Accepted by Judge0 (no runtime/compile error)
        if status_id == 3 or run_result["status_desc"].startswith("Accepted"):
            # Mock mode: always pass (no real execution)
            if actual_stdout == "__MOCK__":
                test_passed = True
                error = None
            else:
                test_passed = (actual_stdout == expected)
                error = None if test_passed else None  # Don't leak expected
        else:
            test_passed = False
            # Compose a safe error message — no expected output revealed
            compile_out = run_result.get("compile_output") or ""
            stderr_out = run_result.get("stderr") or ""
            raw_error = (compile_out or stderr_out or run_result["status_desc"]).strip()
            # Truncate to avoid full code dumps
            error = raw_error[:300] if raw_error else run_result["status_desc"]

        if test_passed:
            passed_count += 1

        results.append({
            "index": i + 1,
            "passed": test_passed,
            "error": error,
        })

    return {
        "passed": passed_count == len(test_cases),
        "total": len(test_cases),
        "passed_count": passed_count,
        "results": results,
    }
