#!/bin/sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
zmk_dir=${1:-"$repo_dir/zmk"}

if [ ! -f "$zmk_dir/app/src/ble.c" ]; then
    echo "ZMK source tree not found at: $zmk_dir" >&2
    exit 1
fi

if grep -q 'Split profile identities require BT_EXT_ADV' "$zmk_dir/app/src/ble.c" &&
    grep -q 'profile_has_connection' "$zmk_dir/app/src/ble.c" &&
    grep -q 'zmk_ble_profile_index_for_conn' "$zmk_dir/app/src/hog.c"; then
    echo "BLE profile identity patch is already applied."
    exit 0
fi

for patch_file in \
    "$repo_dir/patches/zmk-profile-identities-v03.patch" \
    "$repo_dir/patches/zmk-profile-identities-main.patch"; do
    if git -C "$zmk_dir" apply --check "$patch_file" >/dev/null 2>&1; then
        git -C "$zmk_dir" apply "$patch_file"
        echo "Applied BLE profile identity patch to $zmk_dir."
        exit 0
    fi
done

echo "No BLE profile patch applies to this ZMK revision: $zmk_dir" >&2
exit 1
