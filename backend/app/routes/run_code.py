import subprocess
import sys
import tempfile
import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

run_code_bp = Blueprint("run_code", __name__)

TIMEOUT_SECONDS = 5
MAX_CODE_LENGTH = 4000  # chars


@run_code_bp.route("", methods=["POST"])
@jwt_required()
def run_code():
    """
    POST /api/v1/run_code
    Execute a Python code snippet in a sandboxed subprocess.
    Body: { "code": "print('hello')" }
    Returns: { "stdout": "...", "stderr": "...", "exit_code": 0 }
    """
    data = request.get_json(silent=True) or {}
    code = data.get("code", "")

    if not code or not isinstance(code, str):
        return jsonify({"error": "code field is required"}), 400

    if len(code) > MAX_CODE_LENGTH:
        return jsonify({"error": f"Code exceeds maximum length of {MAX_CODE_LENGTH} characters."}), 400

    # Block obviously dangerous patterns
    blocked = ["import os", "import sys", "import subprocess", "__import__",
               "open(", "exec(", "eval(", "compile(", "globals(", "locals(",
               "getattr(", "setattr(", "delattr(", "importlib"]
    for pattern in blocked:
        if pattern in code:
            return jsonify({
                "stdout": "",
                "stderr": f"SecurityError: '{pattern}' is not allowed in the playground.",
                "exit_code": 1,
            }), 200

    # Write to a temp file and run with subprocess
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
            f.write(code)
            tmp_path = f.name

        result = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )

        return jsonify({
            "stdout": result.stdout[:3000],  # Limit output length
            "stderr": result.stderr[:3000],
            "exit_code": result.returncode,
        }), 200

    except subprocess.TimeoutExpired:
        return jsonify({
            "stdout": "",
            "stderr": f"TimeoutError: Code took longer than {TIMEOUT_SECONDS} seconds to run.",
            "exit_code": 1,
        }), 200
    except Exception as e:
        return jsonify({
            "stdout": "",
            "stderr": f"ServerError: {str(e)}",
            "exit_code": 1,
        }), 200
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass
