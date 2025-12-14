import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Optional


def run_submission(
    code: str,
    expected_output: Optional[str] = None,
    expected_input: Optional[str] = None,
) -> Dict[str, object]:
    """
    Execute submitted Python code in a temporary file and optionally compare output.
    This is a simplified runner intended for local demonstration only.
    """

    if not code.strip():
        return {"status": "error", "message": "No code provided."}

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / "submission.py"
        temp_path.write_text(code, encoding="utf-8")

        try:
            completed = subprocess.run(
                ["python", str(temp_path)],
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
                input=expected_input,
            )
        except subprocess.TimeoutExpired:
            return {"status": "error", "message": "Execution timed out."}

    output = completed.stdout
    result: Dict[str, object] = {
        "status": "ok",
        "stdout": output,
        "stderr": completed.stderr,
        "returnCode": completed.returncode,
    }

    if expected_output is not None:
        normalized_expected = expected_output.strip()
        normalized_output = output.strip()
        result["passed"] = normalized_output == normalized_expected
        result["expectedOutput"] = normalized_expected

    return result
