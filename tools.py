import subprocess


def write_file(path, content):
    try:
        with open(path, "w") as f:
            f.write(content)
        return f"wrote {len(content)} bytes to {path}"
    except Exception as e:
        return f"ERROR writing file: {e}"


def read_file(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        return f"ERROR reading file: {e}"

#have menaing ful return statements .
def run_python(filepath):
    try:
        result = subprocess.run(
            ["python3", filepath],
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout + result.stderr
        return output if output.strip() else "ran with no output"
    except Exception as e:
        return f"ERROR running file: {e}"