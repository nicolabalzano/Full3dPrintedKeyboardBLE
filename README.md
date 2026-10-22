# Full 3D Printed Keyboard BLE

<p align="center">
  <img src="images/photo_5897548044184523080_w.jpg" width="32%" />
  <img src="images/photo_5897548044184523082_w.jpg" width="32%" />
  <img src="images/photo_5897548044184523083_w.jpg" width="32%" />
</p>

A fully 3D-printed wireless split keyboard powered by [ZMK Firmware](https://zmk.dev/) running on nice!nano v2 microcontrollers. Features BLE connectivity, dual rotary encoders, OLED displays, and an Italian QWERTY layout with 5 programmable layers.

## Features

- **Wireless split design** -- BLE communication between left (central) and right (peripheral) halves
- **Dual EC11 rotary encoders** -- volume/brightness control on each half
- **OLED displays** -- SSD1306 0.91" 128x32 on each half via I2C
- **OLED status indicators** -- the left display always shows the selected BT profile; the right display shows Caps Lock on/off
- **Battery powered** -- LiPo batteries with BLE power optimized at 0 dBm
- **Italian QWERTY layout** -- designed for Italian OS keyboard layout
- **5 programmable layers**:
  - Layer 0: Base (QWERTY with hold-tap and layer-tap)
  - Layer 1: Accents (Italian vowels and tilde)
  - Layer 2: Symbols & Numpad
  - Layer 3: Functions & Numbers (F1-F12, number row)
  - Layer 4: Gaming Mode (hold-tap disabled for zero latency)
- **Mod-morph behaviors** -- shift-aware punctuation (`'`/`"`, `;`/`:`, `,`/`<`, `.`/`>`)
- **USB fallback** -- wired connection when battery is depleted

## Hardware

| Component | Specification |
|-----------|--------------|
| Microcontroller | nice!nano v2 (nRF52840) |
| Firmware | ZMK |
| Encoders | EC11 rotary encoder x2 |
| Displays | SSD1306 OLED 0.91" 128x32 (I2C) x2 |
| Connectivity | Bluetooth Low Energy (BLE 5.0) |
| Switches | MX-compatible |

## Keymap Layers

### Layer 0: Base (QWERTY)

Standard typing layer with mod-taps on the thumb cluster and layer-taps on specific keys.

```
Left Hand                                       Right Hand
ESC     Q    W    E      R      T               Y      U      I      O      P      BKSP
LSFT    A    S    D      F      G               H      J      K      L      -      ENT
LCTRL   TAB  Z    X      C      V (L3)          B (L3) N      M      ,<     .>     ' (L1)
                  LALT   ! (L2) Win/Spc         Spc    ; (L2) DEL
```

- `V` / `B`: hold to activate Layer 3 (Functions), tap for V / B.
- `'` (Quote): hold to activate Layer 1 (Accents), tap for `'` (Shift: `"`).
- `!` / `;`: hold to activate Layer 2 (Symbols/Numpad), tap for `!` / `;` (Shift on `;`: `:`).
- `,` / `.`: with Shift produce `<` / `>`.
- Thumb encoders: volume and brightness.

### Layer 1: Accents (Italian)

Activated by holding the `'` key. Provides Italian accented vowels and a tilde key (requires Italian OS layout).

```
Left Hand                                       Right Hand
ESC     Q    W    é      è      T               Y      ù      ì      ò      P      BKSP
LSFT    à    S    D      F      G               H      J      K      L      +      ENT
LCTRL   TAB  Z    X      C      V               B      N      M      ~      \      TRANS
                  LALT   !      Spc             Spc    ;      DEL
```

On the accent layer, the key in the comma position types `~` using AltGr+ì
(`RA(EQUAL)` in the keymap); the host operating system must use the Italian
keyboard layout.

### Layer 2: Symbols & Numpad

Activated by holding `!` or `;`. Symbols on the left, numpad and arrows on the right.

```
Left Hand                                       Right Hand
%       |    ^    &      {      }               7      8      9      /      *      BKSP
CAPS    @    $    #      [      ]               4      5      6      +      UP     =
RSFT    RCTRL .   ?      (      )               1      2      3      LEFT   DOWN   RIGHT
                  RALT   WIN    \               0      WIN    DEL
```

### Layer 3: Functions & Numbers

Activated by holding `V` or `B`.

```
Left Hand                                       Right Hand
F1      F2   F3   F4     F5     F6              F7     F8     F9     F10    F11    F12
1       2    3    4      5      6               7      8      9      0      -      -
-       -    TGL4 PSCRN  NUM    -               -      NUM    PSCRN  TGL4   -      -
                  -      -      TGL4            TGL4   -      -
```

- `TGL4`: toggles Layer 4 (Gaming Mode).

### Layer 4: Gaming Mode

Hold-taps disabled for zero latency; WASD prioritized. Toggle with `TGL4` from Layer 3.

```
Left Hand                                       Right Hand
ESC     Q    W    E      R      T               TGL4   U      -      -      BKSP   -
LSFT    A    S    D      F      G               -      -      -      -      -      ENT
LCTRL   TAB  -    1      2      3               4      5      6      7      8      9
                  RALT   Z      Spc             -      -      DEL
```

## Project Structure

```
boards/shields/custom/
  custom.dtsi              # Shared devicetree (encoders, matrix transform)
  custom_left.keymap       # Left half keymap
  custom_left.overlay      # Left half hardware definition
  custom_right.keymap      # Right half keymap
  custom_right.overlay     # Right half hardware definition
config/
  custom_left.conf         # Left half ZMK config (central role)
  custom_right.conf        # Right half ZMK config (peripheral role)
  west.yml                 # Zephyr west manifest
build.yaml                 # GitHub Actions CI build matrix
```

## Building

### Prerequisites

- [Zephyr SDK](https://docs.zephyrproject.org/latest/develop/getting_started/index.html) installed (tested with 0.16.8)
- `west` installed (`pip install west`)
- Initialize the workspace from the project root; the manifest pins the supported ZMK revision and creates the ignored `zmk/` source tree:

```bash
west init -l config
west update --fetch-opt=--filter=tree:0
west zephyr-export
```

### Local build

All build commands run from `zmk/app`. `ZMK_CONFIG` must point to the `config/`
directory of this repository so ZMK picks up `custom_left.conf`,
`custom_right.conf` and the shields in `boards/`:

```bash
cd zmk/app
export ZMK_CONFIG="$PWD/../../config"

# Patch ZMK so each host profile has an independent BLE identity/bond store
"$PWD/../../scripts/apply-zmk-profile-identities.sh" "$PWD/../../zmk"

# Add the Caps Lock indicator and always show the selected BT profile on the left OLED
"$PWD/../../scripts/apply-zmk-display-widgets.sh" "$PWD/../../zmk"

# Recover a stale split BLE bond without deleting any host-device pairings
"$PWD/../../scripts/apply-zmk-split-bond-recovery.sh" "$PWD/../../zmk"

# Left half (central)
west build -d build/left -s . -p -- -DBOARD=nice_nano_v2 -DSHIELD=custom_left \
  -DZMK_CONFIG="$ZMK_CONFIG" -DZMK_EXTRA_MODULES="$PWD/../.."

# Right half (peripheral)
west build -d build/right -s . -p -- -DBOARD=nice_nano_v2 -DSHIELD=custom_right \
  -DZMK_CONFIG="$ZMK_CONFIG" -DZMK_EXTRA_MODULES="$PWD/../.."

# Settings reset image, used when re-pairing after this change
west build -d build/settings_reset -s . -p -- -DBOARD=nice_nano_v2 -DSHIELD=settings_reset \
  -DZMK_CONFIG="$ZMK_CONFIG" -DZMK_EXTRA_MODULES="$PWD/../.."
```

On subsequent builds (CMake cache already configured) you can simply run:

```bash
west build -d build/left -s .
west build -d build/right -s .
west build -d build/settings_reset -s .
```

The firmware images are generated at:

- `zmk/app/build/left/zephyr/zmk.uf2`
- `zmk/app/build/right/zephyr/zmk.uf2`
- `zmk/app/build/settings_reset/zephyr/zmk.uf2`

### GitHub Actions

Push to the repository to trigger automated builds. Download the left, right,
and settings-reset `.uf2` artifacts from the workflow run.

## Flashing

1. Double-click the reset button on the nice!nano to enter bootloader mode
2. Mount the `NICENANO` USB drive
3. Copy the corresponding `.uf2` file:

```bash
# Left half
cp zmk/app/build/left/zephyr/zmk.uf2 /run/media/$USER/NICENANO/

# Right half
cp zmk/app/build/right/zephyr/zmk.uf2 /run/media/$USER/NICENANO/
```

## Pairing the Two Halves

Flash `settings_reset.uf2` on both halves first to clear previous BLE bonds, then flash the firmware. The halves will automatically pair on boot.

To connect to a host device, use the key combos defined in the keymap:
- **ESC + T** (hold 500ms): Clear all BLE bonds
- **M + ,** (hold 100ms): Select BLE profile 0
- **, + .** (hold 100ms): Select BLE profile 1
- **. + quote** (hold 100ms): Select BLE profile 2

Each host profile uses a separate keyboard Bluetooth identity. This lets two
operating systems on the same computer keep independent bonds even when they
share one Bluetooth adapter address. After installing this firmware, remove
the old keyboard pairing from both operating systems and flash the settings
reset image on both halves before pairing again.

The central also requires `CONFIG_BT_EXT_ADV=y`: it keeps the host advertiser's
address separate from identity 0, which scans for and connects to the right half.
Without it, legacy advertising and split scanning conflict when they use different
local identities. Host advertisements still use the legacy packet format.

## License

MIT
