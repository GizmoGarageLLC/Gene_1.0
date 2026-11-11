# Gene head - bill of materials

Everything needed to build the head as currently designed: twin-servo jaw drive,
eye screens (1.75" AMOLED or 2.1" LCD, each with its own skull) and camera pupils, Pi 5 and speakers, battery, crown GPIO bay with an
optional handle or GPIO flashlight (plus a cover for the GPIO well), and the slip-ring neck. `BOM.csv` has the same list for a
spreadsheet. Items marked **(assumed)** were fit-checked against a placeholder
shape of the stated size - check your actual part before buying. The eye and battery options are listed together;
`print/PRINT_LIST.md` has which printed parts go with which option.

## 1. Printed parts

Print-ready files are in `print/parts/` (plates in `print/plates/`): every part is a single clean solid, oriented
flat side down, and reloads watertight. Each plate fits a 250 x 250 mm bed, so any
Creality K2 takes it. Everything in `cad/mocks/` is fit-check geometry,
not a part.

| Part | Qty | File (in `print/parts/`) | Solid vol | On plate |
|---|---|---|---|---|
| Skull v7 (shell, brow, eye barrels, thrust pads, crown-bay ledge, neck screw pilots; v7: 26.5 x 7.5 camera ribbon slots, top window in each barrel + plug pocket above it for the display boards' HDMI/USB, inboard barrel wall open above the camera slot, 4 shelf divots, bracket M3 pilots, U-shaped plate between the eyes, shortened barrel tabs, LCD ledge relief) - **AMOLED eyes**: eye stack 15 mm forward in the barrels | 1 | `01_skull_x1.stl` | 567.4 cm3 | 1 |
| Skull v7 for the **2.1" LCD eyes** instead (the same skull before the eyes came forward) | 1 | `01_skull_LCD_EYES_x1.stl` | 574.0 cm3 | 1 LCD |
| Jaw v5 (hex pocket + bore in each arm for the screw-in pins) | 1 | `02_jaw_x1.stl` | 396.5 cm3 | 2 |
| Jaw pivot pin (hex head + bearing pin + D-shaft; same part both sides) - **100 % infill, PETG or tougher (PA / PA-CF / PC), not PLA** | 2 | `23_jaw_pin_x2.stl` | 5.5 cm3 each | 2 |
| Pi 5 shelf v6 (4 mm standoffs, speaker cradles, 4 cubes on the wings; sits flush with the skull's bottom rim, speaker cradles poking out below) | 1 | `03_pi_shelf_x1.stl` | 48.8 cm3 | 3 |
| Battery tray - **2S2P pack** (power bank: see 4b) | 1 | `04_battery_tray_x1.stl` | 23.4 cm3 | 3 |
| Electronics deck - **2S2P pack** (power bank: see 4b) | 1 | `05_battery_deck_x1.stl` | 17.1 cm3 | 3 |
| Crown insert (fills the top slot; the GPIO ribbon's plug clicks into it from below) | 1 | `13_crown_insert_x1.stl` | 18.7 cm3 | 5 |
| Bridge handle - **optional** | 1 | `17_bridge_handle_OPTIONAL_x1.stl` | 57.7 cm3 | 5 |
| GPIO flashlight - **optional**, instead of the handle (saddle + strap + forehead lamp pod) | 1 | `18_gpio_flashlight_OPTIONAL_x1.stl` | 29.1 cm3 | 7 |
| GPIO cover - **optional**, closes the crown's GPIO well when nothing is plugged in | 1 | `19_gpio_cover_OPTIONAL_x1.stl` | 2.6 cm3 | 7 |
| Eye X insert - **optional**, Halloween cap with a raised X for an eye barrel (either eye) | 1 | `20_eye_x_insert_OPTIONAL_x1.stl` | 25.2 cm3 | - |
| Neck (yoke + tube, turns with the head) | 1 | `14_neck_x1.stl` | 99.5 cm3 | 6 |
| Neck base (bearing housing, bolts to the body) | 1 | `15_neck_base_x1.stl` | 96.7 cm3 | 6 |
| Neck clamp collar | 1 | `16_neck_collar_x1.stl` | 1.9 cm3 | 6 |
| Servo bracket, left (v2, with battery pads) | 1 | `06_servo_bracket_L_x1.stl` | 7.0 cm3 | 4 |
| Servo bracket, right (v2, with battery pads) | 1 | `07_servo_bracket_R_x1.stl` | 7.0 cm3 | 4 |
| Jaw drive hub (same part both sides) | 2 | `08_jaw_drive_hub_x2.stl` | 2.5 cm3 each | 4 |
| AMOLED eye harness (holds the whole board; same part both eyes) - **AMOLED eyes**, **black PETG, 4 walls** | 2 | `25_eye_amoled_harness_x2.stl` | 8.9 cm3 each | 12 |
| Eye display carrier v3 (wide top + bottom slots, side walls only behind the front lip) - **LCD eyes** | 2 | `09_eye_display_carrier_x2.stl` | 2.5 cm3 each | 4 |
| Eye board cradle L and R (handed; hold the LCD and its driver board rigidly, leads tied to the plate; replace the retainer ring) - **LCD eyes**, **PETG, 4 walls** | 1 + 1 | `24_eye_display_cradle_L_x1.stl`, `24_eye_display_cradle_R_x1.stl` | 10.7 cm3 each | 11 |
| Camera bezel v3 (same part both eyes, turned 180 deg; 8.6 x 12.4 pocket for the Arducam, 6.8 mm cable lane on the back) - **print in black** | 2 | `11_camera_bezel_x2.stl` | 5.2 cm3 each | 4 |
| Pupil ring (glues round the camera lens) - **print in black** | 2 | `12_pupil_ring_x2.stl` | 0.3 cm3 each | 4 |

Plates (drop the `.3mf` straight into Creality Print; if the parts don't land
centred, press **Arrange**):

| File | Contents | Footprint | Height |
|---|---|---|---|
| `Plate1_skull.3mf` | skull, AMOLED eyes | 191 x 183 mm | 144 mm |
| `Plate1_skull_LCD_eyes.3mf` | skull, LCD eyes | 191 x 183 mm | 144 mm |
| `Plate2_jaw.3mf` | jaw, 2 jaw pins | 198 x 186 mm | 120 mm |
| `Plate3_shelf_battery.3mf` | shelf, battery tray, deck | 187 x 194 mm | 25 mm |
| `Plate4_small_parts.3mf` | 2 brackets, 2 hubs, 2 carriers (LCD eyes only), 2 bezels, 2 pupil rings | 196 x 197 mm | 28 mm |
| `Plate5_crown_insert_handle.3mf` | crown insert, bridge handle (skip the handle if you don't want it) | 58 x 225 mm | 29 mm |
| `Plate6_neck.3mf` | neck, neck base, clamp collar | 153 x 149 mm | 86 mm |
| `Plate7_gpio_flashlight_cover.3mf` | GPIO flashlight, GPIO cover (both optional) | 86 x 143 mm | 30 mm |
| `Plate8_changes_2026-10-16.3mf` | skull (AMOLED), shelf, eye X insert, for a 350 mm bed | 267 x 301 mm | 144 mm |
| `Plate9_powerbank_tray_deck.3mf` | power bank tray and deck (PETG) | 197 x 81 mm | 32 mm |
| `Plate10_display_carriers.3mf` | the two LCD carriers | 129 x 60 mm | 12 mm |
| `Plate11_eye_cradles.3mf` | eye board cradles L and R, LCD eyes (PETG) | 127 x 65 mm | 32 mm |
| `Plate12_amoled_harnesses.3mf` | the two AMOLED harnesses (black PETG) | 129 x 60 mm | 23 mm |

Print notes:

- **Colour:** print the camera bezels and pupil rings in black (a filament swap, or
  the CFS on a K2). The black spoke then disappears against the dark screen, and
  the lens plus ring read as the pupil.
- **Material:** the two jaw pivot pins in a tough filament: PETG at least, nylon (PA / PA-CF) or PC if your printer can do it, not PLA: they carry the jaw
  and the servo torque, and PLA is brittle there. PETG for the battery tray, deck and both servo brackets, which sit
  next to the pack and carry the drive torque, and for the GPIO flashlight, whose LED gets warm. PLA or PETG is fine for everything else.
- **Supports:** tree supports on plates 1, 2 and 3; none on plate 6. `print/plates/tree_supports/` has copies of the plates that need supports with organic tree supports already set, tuned to come off easily (see `print/PRINT_LIST.md`). The skull's face, the jaw arms,
  and the shelf's plate between the speaker cradles all overhang. The skull's
  new crown ledge sits in the dome ceiling, which needs support anyway. Plate 4
  needs support only under the small screw pads on the brackets. Plate 5: both
  parts print on their sides, so the insert's visible top prints smooth; support
  the handle's grip span and the insert's lower step. Plate 7: the flashlight lies on its
  side (saddle side down) and needs tree supports under the strap and lamp pod; the cover
  prints upright with no supports.
- **Strength:** 4 walls and 20-25 % infill for the jaw, hubs, brackets and handle. The two jaw pins at 100 % infill.
  Everything else prints fine at defaults.
- **Filament:** the parts are 1402 cm3 as solid models (1344 without the optional
  handle). At normal wall and infill settings, expect roughly 0.9-1.1 kg plus
  supports, so have about 1.3 kg on hand. Creality Print's estimate will be more
  accurate.
- The separate `GeneTop_v3_barrel_*.stl` files are **not** needed; the barrels
  are already part of the skull.
- **Neck:** print the neck yoke-down (plate on the bed); no supports. With the neck
  fitted, set the jaw servo limit to **33 deg**: past 35.5 deg the chin swings back
  into the neck base.
- The old twist-lock `GeneHead_top_handle.stl` is retired: the crown slot is now
  filled by the insert, and the bridge handle bolts on top of it instead.

## 2. Hardware

| Item | Qty | Where |
|---|---|---|
| M2 x 12 screw | 8 | Couplers (hubs) to servo horns, 4 per side, fitted on the bench before the servos go in |
| M2 x 8 screw | 8 | Servos to brackets (4 per side) |
| M3 x 5 set screw (grub) | 4 | Hub to D-shaft (2), and one into the back edge of each jaw arm to lock its pivot pin (2) |
| M3 x 16 self-tapping, pan head | 4 | Brackets to skull wall |
| M2 x 16 hex socket head bolt + M2 hex nut | 4 + 4 | Brackets to skull, through-bolted: in from outside the skull (counterbored flush), nut in the hex pocket in each bracket foot (2 per side) |
| M2 x 12 hex socket head bolt + M2 hex nut | 4 + 4 | Pi shelf cubes to the skull: nut dropped into the slot in each cube's top, cube slid up into its divot, bolt in from outside the skull (counterbored flush) (2 per side) |
| M3 x 12 self-tapping, pan head | 4 | Battery tray up through the bracket pads |
| M3 x 10 self-tapping, pan head | 4 | Deck to battery tray |
| M2.5 x 12 screw + M2.5 nut | 4 + 4 | Pi 5 to shelf standoffs (nut under the plate) |
| M2 x 12 hex bolt | 4 | Crown insert down into the skull ledge bosses (no handle) |
| M3 x 16 socket head, self-tapping | 4 | Bridge handle + insert into the ledge bosses (only with the handle) |
| M3 x 20 socket head, self-tapping | 2 | GPIO flashlight + insert, front pair only (only with the flashlight; the rear pair stay M2 x 12 hex bolts) |
| M3 x 16 socket head, self-tapping | 5 | Neck yoke up into the skull's rear rim |
| M3 x 8 self-tapping | 3 | Slip-ring flange to the neck base floor |
| M3 x 10 set screw + M3 nut | 1 + 1 | Clamp collar onto the neck tube (nut in the collar's slot) |
| M3 screw, supplied with the USB-C extension (11 mm) | 2 | Charge port: from outside the skull into the flange |
| M4 bolt (length to suit your body) | 4 | Neck base to the body/stand (76 x 45 mm rectangle) |
| 6808-2RS bearing, 40 x 52 x 7 | 2 | Neck base |
| Hook-and-loop strap, 20-22 mm wide, ~250 mm | 2 | Pack to tray |
| CA glue (medium) | 1 | Display carriers and eye board cradles (LCD) or harnesses (AMOLED), bezels, pupil rings, speakers |
| Zip ties, 2.5 mm wide, short | 4 (LCD) / 2 (AMOLED) | LCD: HDMI and USB leads to each cradle's tie plate. AMOLED: each USB-C lead to its harness tongue |

M3 self-tapping totals: 4 x M3x10, 4 x M3x12 pan head,
9 x M3x16 (plus 4 x M3x16 socket head only if you fit the handle, or 2 x M3x20 socket head for the flashlight), 3 x M3x8. The hubs are drilled 2.2 mm for
M2, but the ROBOTIS model shows the horn holes at 1.6 mm, so check the horn
before final assembly.

## 3. Electronics

| Item | Qty | Notes |
|---|---|---|
| Raspberry Pi 5 (4 or 8 GB) | 1 | 85 x 56 mm board. Mount it with the GPIO header along the front edge (towards the eyes), USB/Ethernet at the -X end |
| Pi 5 Active Cooler | 1 | Stack fit-checked at 14 mm, USB/Ethernet block at 16 mm |
| microSD card, 32 GB+ | 1 | |
| ROBOTIS DYNAMIXEL XL330-M288-T | 2 | Horns included. Run in tandem, **one reversed** |
| DYNAMIXEL TTL interface (ROBOTIS U2D2, or a half-duplex buffer on the Pi UART) | 1 | On the two left shelf cubes, above the left wing (fit-checked at U2D2 size, 48 x 18 x 15), foam tape |
| GPIO 1-to-2 splitter board (2x20) | 1 | On the Pi header: one header for the crown ribbon, one for the I2S amp |
| **LCD eyes:** TekGroAml 2.1" round 480 x 480 LCD + mini-HDMI driver board (Amazon B0DZ2ZKP7B) | 2 | Bought. LCD 56.18 x 59.71 x 2.3 mm (53.28 active) with a 26.9 mm, 40-pin flex off the bottom. Driver board is **round, 57 mm dia**, 4 x M2.5 holes (2.5 mm), mini-HDMI (11.5 wide) and **micro-USB** (8 wide) on the edge opposite the flex connector, each angled 15 deg - so they splay apart. Mount each LCD + board **turned 180 deg** (LCD flex at the top, plugs pointing down) and flip the picture on the Pi with a 180 deg display rotation: flex-down puts the outboard plug only 8-10 mm from the barrel skin. The barrels' inboard walls are open above the camera slot so the LCD ribbon can swing past while you turn it. 5 V 1 A+ |
| **LCD eyes:** eye leads, chenyang CYFPV micro-HDMI to mini-HDMI FPC flat cable, 0.5 m (Amazon B01EWP9EA0) + chenyang micro-USB flat ribbon, USB-A to 90 deg UP-angled micro-USB (Amazon B096YDCSCW / B096YBZCKS) | 2 + 2 | Bought. Each board end is a 90 deg plug on a small flat PCB with a ZIF latch for the 0.1 mm ribbon. Both ribbons must run **back** into the head over the cradle's tie plate: the micro-USB end is UP-angled, but the chenyang HDMI end is DOWN-angled and sends that ribbon forward at the LCD, so swap it for the **NGFF CN-017-UP mini-HDMI UP-angled end** (Amazon B0GZJ41721, 5-pack, bought 2026-11-10; refit the same ribbon). The ribbons tear if creased or pulled: bend them round, never fold them, and zip-tie them to the cradle's plate |
| **AMOLED eyes, instead of the two rows above:** Waveshare ESP32-S3-Touch-AMOLED-1.75 (466 x 466 round AMOLED, capacitive touch, ESP32-S3, one USB-C) | 2 | **Not bought.** **(assumed)** 48.96 dia x 10.4 deep with the USB-C centred on the back (Core Electronics listing): check yours against `eye_amoled.py` before printing the harness. Needs eye firmware on the board (not written yet) |
| **AMOLED eyes:** USB-A to 90 deg USB-C lead, the C end pointing down | 1 x 150 mm + 1 x 200 mm | Left and right eye to the Pi's USB-A ports; power and data on one lead |
| Arducam B0066 mini camera, OV5647 5 MP (Amazon B012QRGUCQ) | 2 | Bought. 8.5 mm square head, ~12 mm long with the crystal behind it; 300 mm, 6 mm wide flex ending in a rigid 16 x 30 mm 15-pin (1 mm pitch) tail |
| Pi 5 CSI cable, 22-pin to 15-pin | 2 | Bought: Wonrabai 200 mm and Waveshare 300 mm. The Arducam's own 300 mm flex passes through the 26.5 x 7.5 mm slot in each barrel. **Both the Arducam end and these cables' 15-pin end are bare flex tails, so joining them needs a 15-pin 1 mm FFC coupler (extension board) per camera - not on the order** |
| Capsule slip ring, 22 mm body, max 30 mm tall, 44 mm flange with 3 holes on 35 mm PCD (e.g. 12-circuit, 2 A) | 1 | **(assumed)** Bolts to the neck base floor; rotating wires run up the 26 mm tube bore into the head, fixed wires leave through the base |
| 40-pin GPIO extension ribbon, female-to-male, 20 cm: UCTRONICS U6033 (Amazon B07D991KMR) | 1 | Bought. Female end on the Pi header. The male end is a standard shrouded 2.54 mm male IDC plug, 61.1 x 8.4 x 13.0 mm (Wurth WR-BHD 612 040 258 21 outline; shroud cavity 56.1 x 6.3), the ribbon leaving one long side near the bottom. It clicks into the crown insert from below, no glue |
| Speaker, 28 mm round, 8 ohm, 1-2 W, 5 mm deep max | 2 | **(assumed)** |
| I2S amplifier, MAX98357A breakout | 1 | Mono: drives both speakers wired in parallel (4 ohm load). The Pi 5 has no analog audio. Flat on the shelf, centred between the speakers, foam tape. Leave SD open on an Adafruit board; on a clone with no SD pull-up add 1 Mohm SD to Vin |

Optional GPIO flashlight (only if you print it):

| Item | Qty | Notes |
|---|---|---|
| 2x20 female pin header, 2.54 mm pitch, 8.5 mm body, standard tails | 1 | Fitted upside down in the saddle, onto the crown pins |
| White LED on a 20 mm aluminium star, 1-3 W class (e.g. Cree XP-G / XP-E) | 1 | Run at about 200 mA (~0.6 W, 60-70 lm), so it stays cool enough in a PETG pod |
| 20 mm LED optic for star LEDs, 30 deg, up to 12.5 mm tall | 1 | Glued into the front of the pod |
| AO3400A logic-level N-MOSFET (SOT-23), on a small adapter or perfboard | 1 | Low-side switch, gate from GPIO 12 |
| 10 ohm 1 W resistor | 1 | Sets about 200 mA from 5 V |
| 100 ohm and 10 kohm resistors | 1 each | Gate series and gate pull-down |
| Perfboard, cut to fit a 16 mm dia x 7 mm cavity | 1 | Behind the LED star |
| 26-28 AWG silicone wire, 3 colours | ~200 mm each | Header tails to the pod, in the channel under the strap |

## 4. Power

| Item | Qty | Notes |
|---|---|---|
| 18650 cell, 3000-3500 mAh, 10 A+ (Samsung 30Q, Molicel P28A) | 4 | Built as 2S2P, 7.2 V, 43-50 Wh |
| Nickel strip + spot welding, or a pre-built 2S2P 18650 pack | 1 | Pack must fit 74.4 x 65 x 18.5 mm plus wrap |
| 2S BMS with balancing, 20 A (HW-391, 48 x 20 x 3 mm) | 1 | Sits in the deck's BMS bay |
| 5 V 5 A step-down converter, Pololu D36V50F5 (25.4 x 25.4 x 9.5 mm) | 2 | One for the Pi (set 5.1 V), one for servos and audio |
| 2S Li-ion USB-C charger board, 5 V in, board max 40 x 20 mm | 1 | Sits in the deck's charger bay |
| Charge port: Poyiccot USB-C male-to-female panel-mount extension, 30 cm, right-angle male (Amazon B086W2R8Z6) | 1 | Bought. Female end mounts **inside** the lower back of the skull (X 0, Z -14), flange (25 x 8, long axis horizontal, M3 holes 16.6 apart side by side) on a flat seat, 2 x M3 from outside into the flange. Right-angle male end plugs into the charger board on the deck. The supplied screws are 11 mm (8 mm into the flange): if they bottom out, use M3 x 8 |
| Power switch (rocker or slide) | 1 | **Location not chosen yet** |
| XT30 connector pair | 1 | Pack to power boards |
| 18 AWG silicone wire (red/black) | ~1 m | Pack, converters, servo rail |
| 22-24 AWG silicone wire | ~1 m | Pi power, signals |
| Heat-shrink assortment | 1 | |

Power budget: about **14 W talking and 36 W peak** from the pack, which gives about
**3 h** of runtime. If the Pi is fed through its GPIO 5 V pins rather than USB-C, add
`usb_max_current_enable=1` to `config.txt` or its USB ports are limited to 600 mA.

### 4b. Secondary setup: bought power bank instead of the pack

Fit-checked instead of the 2S2P pack. Wiring is in [`WIRING.md`](WIRING.md#secondary-setup-bought-power-bank-instead-of-the-2s2p-pack).

| Item | Qty | Notes |
|---|---|---|
| INIU Pocket Rocket P50 power bank, 10000 mAh, 45 W (83.6 x 53.1 x 25.4 mm) | 1 | The tray bay is 84.6 x 54.1. Measure your unit: other banks fit if they are no bigger than that and have a USB-C port that gives **15 V 3 A** on its own |
| USB-C PD trigger board, fixed or set to 15 V, max 32 x 14 x 5 mm | 1 | In the deck's trigger bay |
| Printed: power bank tray `21_battery_tray_POWERBANK_x1.stl` and deck `22_battery_deck_POWERBANK_x1.stl` | 1 each | Instead of parts 04 and 05. PETG. Both print as installed with no supports: the tray floor down (102.8 x 80.6 x 32 mm), the deck plate down |
| M3 x 12 self-tapping, pan head | 2 | Tray up through the **rear** bracket pads |
| M3 x 10 self-tapping, pan head | 2 + 4 | Tray up through the **front** bracket pads (the floor there is only 6 mm thick), and the deck down into the tray posts |
| Foam pad, 1 mm, ~80 x 50 mm | 1 | On top of the bank: the deck clamps the bank down through it |

Still needed from section 4: both D36V50F5 bucks, the charge port extension, the power switch, 18 AWG and 22-24 AWG wire, and heat-shrink. Not needed: the cells, nickel strip, BMS, charger board, XT30 and the two hook-and-loop straps. The fuse can drop to 5 A.

## 5. Cables

Wiring diagrams for the audio chain and the power stack are in [`WIRING.md`](WIRING.md).

Every run was routed through the free space in the head and checked as a solid tube against every part and every other cable, in all four setups (pack + LCD 16 runs, power bank + LCD 17, pack + AMOLED 14, power bank + AMOLED 15; all clear). "Buy" is the route plus 15 % for bends and 30 mm at the connectors, rounded up to a stock length. A run that differs between setups has a row per version. Generated by `cad/tools/bom_tables.py` from `route.py`'s results.

| Cable | Setups | Envelope dia | Route mm | Buy mm | Tightest gap mm |
|---|---|---|---|---|---|
| Pack leads (XT30 + balance) | pack | 6 | 189 | **250** | 0.25 |
| Slip-ring bundle to deck | pack | 6 | 197 | **300** | 0.61 |
| Pi buck -> Pi 5 USB-C | pack | 4 | 175 | **250** | 0.48 |
| Servo buck -> servo R | pack | 3 | 133 | **200** | 0.78 |
| USB: Pi 5 -> TTL interface | all | 4 | 65 | **150** | 0.85 |
| DYNAMIXEL: interface -> servo L | pack | 3 | 77 | **150** | 1.41 |
| DYNAMIXEL: servo L -> servo R | pack | 3 | 47 | **100** | 1.27 |
| Camera L ribbon -> CAM/DISP 0 | LCD eyes | 4 | 131 | **200** | 0.30 |
| Camera R ribbon -> CAM/DISP 1 | LCD eyes | 4 | 151 | **250** | 0.00 |
| Display L -> micro-HDMI 1 | LCD eyes | 4 | 111 | **200** | 0.30 |
| Display R -> micro-HDMI 0 | pack + LCD | 4 | 123 | **200** | 1.43 |
| Display L power -> Pi USB-A | LCD eyes | 4 | 58 | **100** | 1.80 |
| Display R power -> Pi USB-A | LCD eyes | 4 | 136 | **200** | 0.94 |
| Speaker L -> amp | all | 2.5 | 27 | **75** | 2.20 |
| Speaker R -> amp | all | 2.5 | 25 | **75** | 2.45 |
| Amp (I2S) -> GPIO splitter | LCD eyes | 3 | 25 | **75** | 4.94 |
| Charge port -> bank USB-C (extension) | power bank | 4 | 108 | **200** | 0.43 |
| Bank USB-C -> PD trigger | power bank | 4 | 72 | **150** | 0.55 |
| Slip-ring bundle to deck | power bank | 6 | 108 | **200** | 1.96 |
| Pi buck -> Pi 5 USB-C | power bank | 4 | 135 | **200** | 0.44 |
| Servo buck -> servo R | power bank | 3 | 103 | **150** | 0.45 |
| DYNAMIXEL: interface -> servo L | power bank | 3 | 79 | **150** | 1.27 |
| DYNAMIXEL: servo L -> servo R | power bank | 3 | 48 | **100** | 1.27 |
| Display R -> micro-HDMI 0 | power bank + LCD | 4 | 103 | **150** | 0.30 |
| Camera L ribbon -> CAM/DISP 0 | AMOLED eyes | 4 | 144 | **200** | 0.30 |
| Camera R ribbon -> CAM/DISP 1 | AMOLED eyes | 4 | 163 | **250** | 0.00 |
| Eye L USB-C -> Pi USB-A | AMOLED eyes | 4 | 68 | **150** | 2.72 |
| Eye R USB-C -> Pi USB-A | AMOLED eyes | 4 | 147 | **200** | 4.16 |
| Amp (I2S) -> GPIO splitter | AMOLED eyes | 3 | 27 | **75** | 4.94 |
| GPIO ribbon, Pi to crown (female-to-male) | all | flat, 51 wide | ~110 | **200** | 0.3 |

Ribbons and leads were checked with a 4 mm envelope (3 mm for the DYNAMIXEL and servo-power leads, 2.5 mm for the speaker wires, 6 mm for the pack leads and slip-ring bundle). The LCD and AMOLED eye leads, and the Pi power leads into the Pi, run their last few millimetres into the Pi mock, which is a solid block, ports included.

## 6. Not yet designed or placed

- Power switch hole in the skull (the charge port is cut, see `DESIGN_NOTES.md`).
- Wiring for the power switch (once its hole exists), and the slip ring's fixed-side
  wires below the neck base.
- A motor to drive the neck rotation. The exposed tube between the head and the
  neck base has room for a gear or pulley.
- The body or stand the neck base bolts to (4 x M4 on a 76 x 45 mm rectangle).
