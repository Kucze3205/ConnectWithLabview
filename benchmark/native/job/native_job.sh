#!/usr/bin/env bash
# Proposed inspection only; PrintToSingleFileHtml and its parameters are
# unverified for this image. See README.md. Never save, build or execute a VI.
set -euo pipefail
LV_PATH="$1"
shift
finish() {
  LabVIEWCLI -OperationName CloseLabVIEW -LabVIEWPath "$LV_PATH" -Headless > /probe/outputs/logs/close.log 2>&1 || true
}
trap finish EXIT
test -x "$LV_PATH"
command -v LabVIEWCLI
test "$#" -eq 2
dpkg-query -W -f='${Package} ${Version}\n' 'ni-labview-2026*' > /probe/outputs/logs/installed-version.txt
test -s /probe/outputs/logs/installed-version.txt
index=0
for relative in "$@"; do
  case "$relative" in
    pylavi/tests/empty_separate_code.vi|pylavi/tests/empty_no_debugging.vi) ;;
    *) exit 64 ;;
  esac
  printf -v ordinal '%02d' "$index"
  test -s "/probe/inputs/$relative"
  # Operation, VIPath and HTMLFilePath are unverified; do not infer typed
  # properties or actual diagram capture from successful exit or HTML alone.
  LabVIEWCLI -LogToConsole TRUE \
    -LogFilePath "/probe/outputs/logs/print-$ordinal.log" \
    -OperationName PrintToSingleFileHtml \
    -VIPath "/probe/inputs/$relative" \
    -HTMLFilePath "/probe/outputs/reports/$ordinal.html" \
    -LabVIEWPath "$LV_PATH" -Headless \
    > "/probe/outputs/logs/console-$ordinal.log" 2>&1
  test -s "/probe/outputs/reports/$ordinal.html"
  index=$((index + 1))
done
