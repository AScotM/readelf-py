import subprocess
import shutil
import sys
import os

def readelf_header_parsed(path):
    if not shutil.which("readelf"):
        raise RuntimeError("readelf not found in PATH - please install binutils")
    
    if not os.path.exists(path):
        raise RuntimeError(f"File not found: {path}")
    
    try:
        result = subprocess.run(
            ["readelf", "-h", path],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        err = e.stderr.strip() if e.stderr else str(e)
        raise RuntimeError(f"readelf failed on {path}: {err}") from e

    data = {}
    for line in result.stdout.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            parts = value.split()
            
            if key == "Machine" and parts:
                value = parts[0]
            elif key == "Size of this header" and parts:
                value = parts[0]
                
            data[key] = value

    return data

if __name__ == "__main__":
    try:
        info = readelf_header_parsed("/bin/ls")
        for k, v in info.items():
            print(f"{k}: {v}")
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
