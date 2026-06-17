"""
Intentionally vulnerable example code.

This module exists ONLY to give the SAST scanner (Semgrep) something to flag.
Each function documents the weakness it demonstrates and how it should be fixed.
DO NOT use any of these patterns in real code.
"""

import hashlib
import os
import sqlite3
import subprocess


# ---------------------------------------------------------------------------
# 1. Hardcoded secret (Semgrep: generic.secrets / detected-credentials)
#    Fix: load from environment variables or a secrets manager (e.g. Vault).
# ---------------------------------------------------------------------------
API_KEY = "EXAMPLE_FAKE_API_KEY_PLACEHOLDER_1234"  # nosec - demo only


# ---------------------------------------------------------------------------
# 2. SQL injection (Semgrep: python.lang.security.sql-injection)
#    Fix: use parameterized queries (placeholders), never string formatting.
# ---------------------------------------------------------------------------
def get_user(user_id: str) -> list:
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # VULNERABLE: user input concatenated directly into the query.
    query = "SELECT * FROM users WHERE id = '" + user_id + "'"
    cursor.execute(query)
    return cursor.fetchall()


# ---------------------------------------------------------------------------
# 3. Command injection (Semgrep: dangerous-subprocess-use)
#    Fix: avoid shell=True; pass arguments as a list.
# ---------------------------------------------------------------------------
def ping_host(host: str) -> int:
    # VULNERABLE: shell=True with unsanitized input allows command chaining.
    return subprocess.call("ping -c 1 " + host, shell=True)


# ---------------------------------------------------------------------------
# 4. Weak hashing algorithm (Semgrep: insecure-hash-algorithm)
#    Fix: use hashlib.sha256 (or a password hash like bcrypt/argon2).
# ---------------------------------------------------------------------------
def hash_password(password: str) -> str:
    # VULNERABLE: MD5 is cryptographically broken.
    return hashlib.md5(password.encode()).hexdigest()


# ---------------------------------------------------------------------------
# 5. Use of eval on external input (Semgrep: eval-detected)
#    Fix: never eval untrusted input; use ast.literal_eval or proper parsing.
# ---------------------------------------------------------------------------
def calculate(expression: str):
    # VULNERABLE: arbitrary code execution.
    return eval(expression)  # noqa: S307


if __name__ == "__main__":
    # Demonstration entrypoint (not meant to be run in production).
    print("This is an intentionally vulnerable demo module.")
    print("Environment:", os.environ.get("APP_ENV", "dev"))
