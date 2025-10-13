import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def run(rel_path: str):
    script = ROOT / rel_path
    print("\n>>>", sys.executable, str(script))
    subprocess.run([sys.executable, str(script)], check=True, cwd=str(ROOT))

if __name__ == "__main__":
    run("tests/smoke_db.py")
    run("tests/test_queries.py")
    run("tests/test_negative.py")
    print("\n✅ All tests completed successfully.")
