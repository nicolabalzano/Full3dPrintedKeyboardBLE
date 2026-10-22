#!/bin/sh
# Rigenera i font LVGL usati dal display della tastiera.
#
# Serve a due font concatenati (catena di fallback):
#   custom_montserrat_ui_N  -> testo Montserrat peso 550
#   custom_symbols_ui_N      -> glifi LV_SYMBOL_* presi da FontAwesome 5
#
# I font Montserrat inclusi in LVGL NON contengono i codepoint dei simboli
# (U+F00C, U+F00D, U+F1EB, ...), quindi senza il fallback le icone dello
# status screen vengono disegnate come rettangoli vuoti.
#
# Requisiti: python3 con fontTools, node/npx (lv_font_conv), curl.
# I .c generati sono committati, quindi per compilare il firmware non serve
# eseguire questo script.
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
work_dir=${1:-/tmp/kbfonts}
fonts_dir="$repo_dir/src/display/fonts"

mkdir -p "$work_dir"

# 1. Font variabile Montserrat -> istanza statica a peso 550
if [ ! -f "$work_dir/Montserrat-550.ttf" ]; then
    curl -fsSL -o "$work_dir/Montserrat-VF.ttf" \
        "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat%5Bwght%5D.ttf"
    python3 -m fontTools.varLib.instancer "$work_dir/Montserrat-VF.ttf" wght=550 \
        -o "$work_dir/Montserrat-550.ttf"
fi

# 2. FontAwesome 5 -> TTF con upem 640, cosi' le icone riempiono l'em
if [ ! -f "$work_dir/FontAwesome5-640.ttf" ]; then
    curl -fsSL -o "$work_dir/FontAwesome5.woff" \
        "https://raw.githubusercontent.com/lvgl/lvgl/v8.3.11/scripts/built_in_font/FontAwesome5-Solid%2BBrands%2BRegular.woff"
    python3 - "$work_dir" <<'PY'
import sys
from fontTools.ttLib import TTFont
from fontTools.ttLib.scaleUpem import scale_upem
work = sys.argv[1]
f = TTFont(f"{work}/FontAwesome5.woff")
scale_upem(f, 640)
f.save(f"{work}/FontAwesome5-640.ttf")
PY
fi

# 3. Generazione dei font LVGL
SYMS=0xF00C,0xF00D,0xF013,0xF026,0xF0E7,0xF1EB,0xF240,0xF241,0xF242,0xF243,0xF244,0xF287,0xF293

for size in 12 16; do
    npx --yes lv_font_conv@1.5.3 --no-compress --no-prefilter --bpp 4 --size "$size" \
        --font "$work_dir/FontAwesome5-640.ttf" -r "$SYMS" \
        --format lvgl --lv-include lvgl.h --lv-fallback "lv_font_montserrat_$size" \
        -o "$fonts_dir/custom_symbols_ui_$size.c"

    npx --yes lv_font_conv@1.5.3 --no-compress --no-prefilter --bpp 4 --size "$size" \
        --font "$work_dir/Montserrat-550.ttf" -r 0x20-0x7E,0xB0 \
        --format lvgl --lv-include lvgl.h --lv-fallback "custom_symbols_ui_$size" \
        -o "$fonts_dir/custom_montserrat_ui_$size.c"

    # lv_font_conv non emette la dichiarazione per i font di fallback personalizzati
    sed -i "s|#include \"lvgl.h\"|#include \"lvgl.h\"\nLV_FONT_DECLARE(custom_symbols_ui_$size);|" \
        "$fonts_dir/custom_montserrat_ui_$size.c"
done

echo "Font generati in $fonts_dir"
