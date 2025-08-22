set -euo pipefail

# /workspace is your project root (mounted with -v "$PWD":/workspace)
SRC_DIR="/workspace/lambdas"
OUT_DIR="/workspace/build"

rm -rf "${OUT_DIR}"
mkdir -p "${OUT_DIR}"
mkdir -p /tmp/pkg

zipdir () {
python - "$1" "$2" <<'PY'
import os, sys, zipfile
src, out = sys.argv[1], sys.argv[2]
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk(src):
        for f in files:
            p = os.path.join(root, f)
            z.write(p, os.path.relpath(p, src))
print(f"Zipped {src} -> {out}")
PY
}

echo "[1/3] Package uploader.zip"
rm -rf /tmp/pkg/uploader && mkdir -p /tmp/pkg/uploader
cp "${SRC_DIR}/uploader/app.py" /tmp/pkg/uploader/
if [ -f "${SRC_DIR}/uploader/requirements.txt" ]; then
  python -m pip install --upgrade pip >/dev/null
  pip install -r "${SRC_DIR}/uploader/requirements.txt" -t /tmp/pkg/uploader >/dev/null
fi
zipdir /tmp/pkg/uploader "${OUT_DIR}/uploader.zip"

echo "[2/3] Package resizer.zip (with Pillow wheels)"
rm -rf /tmp/pkg/resizer && mkdir -p /tmp/pkg/resizer
cp "${SRC_DIR}/resizer/app.py" /tmp/pkg/resizer/
python -m pip install --upgrade pip >/dev/null
pip install -r "${SRC_DIR}/resizer/requirements.txt" -t /tmp/pkg/resizer >/dev/null
zipdir /tmp/pkg/resizer "${OUT_DIR}/resizer.zip"

echo "[3/3] Artifacts ready:"
ls -lh "${OUT_DIR}"
