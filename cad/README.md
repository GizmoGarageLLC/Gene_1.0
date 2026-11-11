# CAD sources and build scripts

All STLs here are in their design frame. `cad/tools/parts.py` places each one in the **head frame**: the X axis is the jaw pivot, the origin is on that axis, -Y is the face (front), and +Z is up. The robot faces -Y, so Gene's own left is +X.

The print-ready copies in `../print/` are the same parts, reoriented flat side down.

## Files

| Kind | Files |
|---|---|
| Skull | `skull.stl` (v7, AMOLED eyes: eyes 15 mm forward) and `skull_lcd.stl` (v7 for the 2.1" LCD eyes: the same skull before `skull_v7_eyes_forward.py`, frozen). Its build scripts start from the v6 skull, `GeneTop_v6_neck.stl`, which is no longer in the folder (see below) |
| Jaw | `jaw.stl`, `jaw_pin.stl` (the two screw-in pivot pins; the right one is the same part turned 180° about Z) |
| Jaw drive | `servo_bracket_L.stl`, `servo_bracket_R.stl`, `jaw_drive_hub.stl` |
| Eyes | `eye_display_carrier.stl`, `eye_display_cradle_L.stl` / `_R.stl` (`tools/eye_cradle.py`; handed, replace `eye_display_retainer.stl`), `camera_bezel.stl`, `pupil_ring.stl`; optional `eye_x_insert.stl` (`tools/eye_x_insert.py`). For the 1.75" AMOLED eyes, `eye_amoled_harness.stl` (`tools/eye_amoled.py`) replaces the carrier and cradle |
| Interior | `pi_shelf.stl`, `battery_tray.stl`, `battery_deck.stl`; for the power bank setup, `battery_tray_pb.stl` and `battery_deck_pb.stl` instead of the last two |
| Crown | `crown_insert.stl`, `bridge_handle.stl`, `gpio_flashlight.stl`, `gpio_cover.stl` |
| Neck | `neck.stl`, `neck_base.stl`, `neck_collar.stl` |
| Fit-check only | `mocks/`: stand-ins for the bought parts (Pi 5, displays, cameras, battery, boards, servos, speakers, slip ring and so on), used by the sim and the clearance checks. **Do not print these** |

## Setup

```
pip install -r tools/requirements.txt
```

Run every script from inside `cad/tools/`, because several open their data files by relative path:

```
cd cad/tools
python check.py
```

## Scripts

| Script | What it does |
|---|---|
| `parts.py` | Loads every current part and places it in the head frame (imported by the others) |
| `check.py`, `sweep.py` | Pairwise interference check of the assembly; jaw sweep against every part |
| `check_v7.py` | Skin left over the v7 eye pockets, ribbon-slot opening, and free height above the display boards |
| `mass.py` | Mass, centre of mass and jaw-servo torque estimate |
| `occ_all.py`, `route.py` | Occupancy grid of the assembly, then a cable routing check for every run in `cables.json` |
| `printprep.py` → `plates.py` | Orients every part for printing (writes `printparts.pkl` and `cad/print/`), then lays out the `.3mf` plates |
| `support_plates.py` | Optional copies of `../print/plates/*.3mf` in `../print/plates/tree_supports/`, with per-object Creality Print (Orca) support settings: organic trees on the parts that need them, tuned to break away easily; off on the rest |
| `battery_powerbank.py` | Secondary power setup: tray, deck and mocks for a bought power bank (INIU P50) instead of the 2S2P pack. Writes its two print files straight to `print/parts/` |
| `eye_amoled.py` | AMOLED eyes: the harness for a Waveshare ESP32-S3-Touch-AMOLED-1.75 board (`eye_amoled_harness.stl`, same part both eyes), its mock with the USB-C plug (`mocks/display_amoled175.stl`), and `print/parts/25` + Plate 12. Board size and USB-C position are assumed; they are parameters at the top |
| Setups | `GENE_POWER=powerbank` and/or `GENE_EYES=amoled` pick a setup (the eyes also pick the skull: `SKULL` and `eye_dy` in `parts.py`) for `check.py`, `occ_all.py`, `route.py` and `mass.py`. Results carry the setup's suffix: `static.json` / `_pb` / `_am` / `_pb_am`, likewise `occ_all*.npz`, `cables*.json`, `mass*.json`. Run all four setups before `export.py` |
| `bom_tables.py` | Rewrites the cable table in `docs/BOM.md` section 5 from all four setups' `cables*.json`, then writes `docs/BOM.csv` from every table in `BOM.md`. Run after `route.py` for all four setups |
| `export.py` → `build_local_sim.py` | Exports meshes (plus the parts that differ per setup, as `<id>_pb.json` / `<id>_am.json`), the jaw sweep and every setup's checks, cables and weights to `web/`, then inlines `web/` into one self-contained `sim/head_sim.html` with a Setup switch. Run `export.py` with no `GENE_*` set |

The skull is built in twelve steps. Run them in this order:

1. `skull_v7.py`: v6 plus the camera ribbon slots, the top display windows and the plug pockets
2. `skull_v7_mirror_eye.py`: makes the right eye's plug pocket an exact mirror of the left one
3. `skull_v7_seal_corners.py`: seals the small holes at the outboard bottom corners of the eye barrels
4. `skull_v7_barrel_taper.py`: blends the back end of each eye barrel into the skull
5. `skull_v7_open_inboard.py`: opens the inboard wall of each eye barrel above the camera slot, so the display ribbon can swing past when the screen is turned 180°
6. `skull_v7_usbc_port.py`: cuts the USB-C charge port (flange seat, opening and 2 x M3 holes) in the lower back wall (flange horizontal), and writes `mocks/usbc_panel.stl`
7. `motor_mount_m2.py`: M2 through-bolt holes (counterbore outside, clearance, hex nut pocket) through the skull wall into both servo bracket feet, and the dia 2.5 pilots for the bracket M3 self-tappers. It changes the two bracket files too

8. `skull_v7_shelf_divots.py`: 4 divots (grooves open at the bottom rim) in the inner wall, and 4 cubes on the Pi shelf wings that slide up into them; M2 x 12 in from outside the skull into a nut dropped into each cube. It changes `pi_shelf.stl` too
9. `skull_v7_eye_plate_window.py`: cuts the flat plate between the eye barrels to a U (6 mm strips along both barrels and the face, open at the back); also updates `../print/parts/01_skull_x1.stl` and Plates 1 and 8
10. `skull_v7_shorten_tabs.py`: cuts the inboard tabs of the eye barrels (the lower arcs behind the camera slots) back to half their length; also updates `../print/parts/01_skull_x1.stl` and Plates 1 and 8
11. `skull_v7_ledge_relief.py`: relief inside the top of each eye barrel for the LCD's flex ledge, keeping 1.1 mm of wall under the skin; also updates `../print/parts/01_skull_x1.stl` and Plates 1 and 8. **The result is the LCD-eyes skull**, kept as `skull_lcd.stl` (`../print/parts/01_skull_LCD_EYES_x1.stl`, `Plate1_skull_LCD_eyes.3mf`)
12. `skull_v7_eyes_forward.py`: the AMOLED-eyes skull. Moves the barrel ridge 15 mm forward, opens the bore behind it, runs the ledge relief and camera-ribbon slots forward; checks the outside is unchanged from 13 directions. Also updates `../print/parts/01_skull_x1.stl` and Plates 1 and 8

A change to the shared skull (anything but the eye barrels' insides) now has to go into both skulls: apply it to `skull_lcd.stl` too, and rewrite its print part and plate.

Steps 2–12 save a copy of their input in `tools/retired/` the first time they run, and read from it on later runs.

`skull.stl` and `skull_lcd.stl` are the only skulls kept in the repo. Step 1 and `check_v7.py` read the v6 skull, which has been removed; to rebuild from step 1, restore it with `git checkout 8078433 -- cad/GeneTop_v6_neck.stl`. All old part versions in `tools/retired/` were deleted too (the skull, jaw and bracket copies), so rerunning a single step now starts from the finished part rather than its original input.

Part generators: `jaw_fill_pivot_holes.py` (filled the old pivot-screw holes in the jaw; already applied), `jaw_screw_pins.py` (jaw v5: cuts the pivot pins off the jaw into `jaw_pin.stl` and puts a hex pocket, bore and grub hole in each arm; reads `tools/retired/jaw_v4_before_screw_pins.stl`), `cam3_arducam.py` (camera bezel v3), `carrier_ease_seat.py` (opens the display seat in the carrier from 56.00 to 56.60 and runs the slots up to the lip for the LCD's flex ledge, so the LCD isn't squeezed; reads `retired/carrier_v3_before_seat_ease.stl`), `carrier_topslot.py` (display carrier v3; its input `retired/carrier_v1_before_topslot.stl` was removed, so restore it with `git checkout 8078433 -- cad/tools/retired/carrier_v1_before_topslot.stl` before rerunning), `pupil.py`, `crown_idc_snap.py` (the GPIO ribbon's shrouded IDC plug clicks into the crown insert: end hooks, a lip on top, side walls clear of the ribbon; reads `tools/retired/crown_insert_before_idc_snap.stl` and rewrites `crown_meta.json`, so rerun `gpio_mocks.py` and `gpio_flashlight.py` after it), `gpio_flashlight.py`, `gpio_mocks.py`, `dboard_mock.py` (flex-down board mock; superseded by `eye_cradle.py`, which writes the turned board mock, the real LCD outline and the cradle, its print file and Plate 11; it fits the cradle to `skull_lcd.stl`), `eye_amoled.py` (the AMOLED harness, its print file and Plate 12).

`battery.py`, `crown.py`, `neck.py` and `shelf6.py` generated their parts at earlier stages of the skull (v4/v5). They are kept as the record of how those parts were made, but they need skull files that are not in this repo. Their output STLs are included and current.

`printprep.py` and `plates.py` write to `cad/print/` (the AMOLED skull only; the LCD skull's print files are kept as they are), which is ignored by git. Copy the results into `../print/parts` and `../print/plates` (the files there use numbered names) when you update the print files.
