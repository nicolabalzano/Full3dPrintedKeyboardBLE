#!/bin/sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
zmk_dir=${1:-"$repo_dir/zmk"}

if [ ! -f "$zmk_dir/app/src/display/status_screen.c" ]; then
    echo "ZMK source tree not found at: $zmk_dir" >&2
    exit 1
fi

if grep -q 'zmk_widget_hid_indicators_init' "$zmk_dir/app/src/display/status_screen.c" &&
    grep -q 'LV_SYMBOL_WIFI : LV_SYMBOL_CLOSE' \
        "$zmk_dir/app/src/display/widgets/output_status.c" &&
    grep -q 'zmk_ble_active_profile_index()' \
        "$zmk_dir/app/src/display/widgets/output_status.c" &&
    grep -q 'custom_montserrat_ui_16' "$zmk_dir/app/src/display/status_screen.c" &&
    grep -q 'set_status_text' \
        "$zmk_dir/app/src/display/widgets/hid_indicators.c" &&
    grep -q 'sync_peripheral_hid_indicators_work' \
        "$zmk_dir/app/src/split/bluetooth/central.c"; then
    echo "Display widget patch is already applied."
    exit 0
fi

for patch_file in \
    "$repo_dir/patches/zmk-display-widgets-v03.patch" \
    "$repo_dir/patches/zmk-display-widgets-main.patch"; do
    if git -C "$zmk_dir" apply --check "$patch_file" >/dev/null 2>&1; then
        git -C "$zmk_dir" apply "$patch_file"
        echo "Applied display widget patch to $zmk_dir."
        exit 0
    fi
done

echo "No display widget patch applies to this ZMK revision: $zmk_dir" >&2
exit 1
