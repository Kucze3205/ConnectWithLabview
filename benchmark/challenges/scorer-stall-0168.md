# scorer-stall-0168: does importing or running score.py stall?

Measurement only; no fix applied. No LabVIEW or native behaviour is claimed.

Copies exported by `.session/artifacts/export_0168.py` (run with `python3 -I`):
- 739 version: `git show 5db2610e:benchmark/scripts/score.py` (the local ref `task/739` does not exist; the commit id from the issue does), saved as `.session/artifacts/score_739_0168.py.txt`, 21947 bytes.
- main version: `git show HEAD:benchmark/scripts/score.py`, saved as `.session/artifacts/score_main_0168.py.txt`, 20858 bytes.

## Static scan

Scanned with `.session/artifacts/scan_0168.py` (regex for `input(`, `stdin`, `subprocess`, `socket`, `urllib`, `sleep`, `while True`, `os.walk`, `rglob`, `glob(`, top-level imports, top-level calls and assignments with calls, `__name__`). A Grep pass over both copies returned no matches, so the scan script was used instead.

- 739 version: none found. Module-level code is only imports (lines 9-15), `ROOT = Path(__file__).resolve().parents[2]` (17), `FIXTURES` (19) and `CATEGORIES` (22). The only entry call is under `if __name__ == '__main__':` (line 404).
- main version: none found. Same module-level lines (9-15, 17, 19, 22). Entry guard at line 391.

## Probe results

Probe: `.session/artifacts/stall_probe_0168.py`. It calls `faulthandler.dump_traceback_later(20, exit=True)`, reopens stdin on `os.devnull`, and execs the source with `__file__` set to the absolute path of `benchmark/scripts/score.py`. In `gen` mode it calls `generate()`. `main()` was never called. The 20 s faulthandler guard applied to every run, including `gen`; no separate 60 s guard was added. Every run finished inside 20 s, so no traceback was produced.

| Version | Mode | Command | Exit | Last output line | Timeout frames |
|---|---|---|---|---|---|
| 739 | import | `python3 -I .session/artifacts/stall_probe_0168.py .session/artifacts/score_739_0168.py.txt` | 0 | `imported` | none |
| main | import | `python3 -I .session/artifacts/stall_probe_0168.py .session/artifacts/score_main_0168.py.txt` | 0 | `imported` | none |
| main | gen | `python3 -I .session/artifacts/stall_probe_0168.py .session/artifacts/score_main_0168.py.txt gen` | 0 | `records 9` | none |
| 739 | gen | `python3 -I .session/artifacts/stall_probe_0168.py .session/artifacts/score_739_0168.py.txt gen` | 0 | `records 9` | none |

## Cause

not found. Neither version stalled on import or on `generate()` under this probe, and the static scan found nothing that can block. The stall in #743 and #747 was not reproduced.

Differences between this probe and the #747 script that could matter, none of them tested: #747 loaded the file through `importlib` from its real path rather than `exec` of a copied source. The stall could also come from the runner (for example stdout handling when printing FIXTURES) rather than from score.py.

Method for the finish task: use the probe above (faulthandler guard, stdin on devnull, `exec` of the source, `python3 -I`), which returned promptly for both versions. Avoid an importlib load-and-print helper as the first step. If a stall recurs, the faulthandler traceback will name the frame. This measurement shows only that import and `generate()` finish for both versions; it does not show the 739 change is otherwise correct.
