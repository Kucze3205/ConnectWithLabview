"""Land the #258 native job design from tag iter/0036/258 onto the current checkout.

Idempotent and hash-gated: copies only the four design files, never touches
preparation JSON, cases, challenges or loop data. Run from the repository root:
    python3 -I execution/scripts/land_native_258.py
Delete this script after the landing merges.
"""
import hashlib
import pathlib
import subprocess
import sys

TAG = "iter/0036/258"
FILES = {
    "benchmark/scripts/native_jobs.py": "081040ce35f2916ef851cea9f96750a5b43f6486408d29f8cca34a6de402655a",
    "benchmark/native/README.md": "78a54100473259a7feaf7dc4684cda1a96836f93b1fd94d200d21b93415376d2",
    "benchmark/native/recipes.json": "f292d56ebfe8428f4f37b589666feebc321136b4cbc26ea51cc27e389d6179e8",
    "benchmark/native/output-record.template.json": "86ba84aaef63a327bc53868622e0b085b49352ed1b220e7481f73f7aac9ec9c7",
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    root = pathlib.Path.cwd()
    for rel, want in FILES.items():
        path = root / rel
        if path.exists() and sha(path.read_bytes()) == want:
            print("ok", rel)
            continue
        data = subprocess.run(["git", "show", f"{TAG}:{rel}"], capture_output=True, check=True).stdout
        if sha(data) != want:
            sys.exit(f"hash mismatch in tag for {rel}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        print("wrote", rel)
    r = subprocess.run([sys.executable, "-I", "benchmark/scripts/native_jobs.py", "--check"])
    if r.returncode:
        sys.exit("native_jobs.py --check failed")
    print("landed", len(FILES), "files")


if __name__ == "__main__":
    main()
