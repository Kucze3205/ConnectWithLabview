# Author four controlled pairs

1. Use one LabVIEW version for all eight files. Any single consistent version is acceptable if recorded. The original `add.vi` in [delivery.md](../delivery.md) declares LabVIEW 21.0; it is background evidence, not a template to patch.
2. Create `docs/research/poc/pair/fixtures/` for the files below. Do not overwrite any original fixture.
3. Start `authoring.md` in that folder. Record the full LabVIEW version, build, bitness, operating system, and date. Record all save settings, including debugging, optimization, save-for-previous use, and separate compiled code. Do not save for a previous version. Keep these settings fixed except for the separate-code variants below.
4. Create a new blank VI. Set two numeric controls named `x` and `y` to representation I32. Wire `x` to the upper input of Add and `y` to its lower input. Wire the output to one I32 indicator named `result`. Add no other nodes.
5. Disable “Separate compiled code from source file” in VI Properties. Leave password protection off for every file. Save as `add-normal.vi` in the folder.
6. Use Save As to create a copy named `subtract-normal.vi`. Replace Add with Subtract using the Replace menu. Preserve the controls, indicator, input order, terminal connections, and wires. Save. Record that this pair's only intended diagram change is Add to Subtract. If any wire changes or breaks, recreate this copy from the baseline.
7. Reopen `add-normal.vi`. Save a copy as `add-separate.vi`. Enable “Separate compiled code from source file” in VI Properties and save it. Record this setting.
8. Copy `add-separate.vi` to `subtract-separate.vi` using Save As. Make only the same Add to Subtract replacement from step 6. Keep separate compiled code enabled and save.
9. Create a second blank VI. Place one numeric constant with representation I32 and value 1. Wire it directly to one I32 indicator. Add no other nodes. Disable separate compiled code and save as `constant-1-normal.vi`.
10. Save a copy as `constant-2-normal.vi`. Change only the constant value from 1 to 2. Keep its representation, indicator, and wire unchanged. Save.
11. Reopen `constant-1-normal.vi`. Save a copy as `constant-1-separate.vi`. Enable separate compiled code and save. Copy that file using Save As to `constant-2-separate.vi`, change only the constant value to 2, and save.
12. In `authoring.md`, list each filename, its separate-code setting, its source baseline, and the exact change. Confirm that every file has no password. Note any load warnings, automatic conversions, or unintended changes; do not silently accept them as a controlled pair.
13. Close the VIs. Supply the eight saved VIs and `authoring.md` together in the folder. Freeze their hashes using [protocol.md](protocol.md) before comparison. Do not resave them after hashing.

These files will measure encoding and dependent saved changes. They do not by themselves prove a valid future edit or LabVIEW behavior. This research session cannot run LabVIEW or author these files.
