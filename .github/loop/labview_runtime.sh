#!/usr/bin/env bash
# Environment smoke only: compile a disposable copy of an existing public VI.
# No source authoring, model process, desktop activation or external network.
set -euo pipefail
LV_PATH="$1"
finish() {
  LabVIEWCLI -OperationName CloseLabVIEW -LabVIEWPath "$LV_PATH" -Headless > /probe/close.log 2>&1 || true
  find /tmp -maxdepth 1 -type f -iname '*labview*headless*' -exec cp -- '{}' /probe/ \; || true
}
trap finish EXIT
test -x "$LV_PATH"
command -v LabVIEWCLI
dpkg-query -W -f='${Package} ${Version}\n' 'ni-labview-2026*' > /probe/installed-version.txt
test -s /probe/installed-version.txt
test -s /probe/fixtures/empty_vifile.vi
LabVIEWCLI -LogToConsole TRUE -LogFilePath /probe/masscompile.log \
  -OperationName MassCompile -DirectoryToCompile /probe/fixtures \
  -LabVIEWPath "$LV_PATH" -Headless 2>&1 | tee /probe/console.log
grep -F 'MassCompile operation succeeded' /probe/console.log
