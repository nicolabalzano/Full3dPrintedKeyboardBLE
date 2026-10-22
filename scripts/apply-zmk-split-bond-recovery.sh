#!/bin/sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
zmk_dir=${1:-"$repo_dir/zmk"}

if [ ! -f "$zmk_dir/app/src/ble.c" ]; then
    echo "ZMK source tree not found at: $zmk_dir" >&2
    exit 1
fi

if grep -q 'Cleared split BLE bond after security failure' "$zmk_dir/app/src/ble.c" &&
    grep -q 'Cleared split BLE bond after security failure' \
        "$zmk_dir/app/src/split/bluetooth/peripheral.c"; then
    echo "Split BLE bond recovery patch is already applied."
    exit 0
fi

patch_file="$repo_dir/patches/zmk-split-bond-recovery.patch"
if git -C "$zmk_dir" apply --check "$patch_file" >/dev/null 2>&1; then
    git -C "$zmk_dir" apply "$patch_file"
    echo "Applied split BLE bond recovery patch to $zmk_dir."
    exit 0
fi

echo "Split BLE bond recovery patch does not apply to this ZMK revision: $zmk_dir" >&2
exit 1
