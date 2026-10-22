These generated LVGL fonts are two chained fonts:

- `custom_montserrat_ui_12/16.c` - Montserrat at weight 550 (instanced from the
  variable font) for the text glyphs (ASCII 0x20-0x7E plus 0xB0). This is a
  little heavier than the original Medium weight.
- `custom_symbols_ui_12/16.c` - FontAwesome 5 with the LVGL symbol glyphs
  (LV_SYMBOL_WIFI, OK, CLOSE, CHARGE, BATTERY_*, USB, SETTINGS, BLUETOOTH,
  ...). The Montserrat fonts shipped with LVGL do NOT contain those code
  points, so without this fallback the status screen icons are drawn as
  empty boxes.

The Montserrat font declares the symbols font as its fallback, and the
symbols font falls back to the built-in Montserrat, so any glyph resolves.

The fonts are 4 bpp: the SSD1306 panel is 1 bit, and a 1 bpp primary font
mixed with a 4 bpp fallback breaks the symbol rendering.

Regenerate everything with:

    ./build-fonts.sh [work_dir]

The script downloads Montserrat (variable) and FontAwesome 5, instances
Montserrat at weight 550, scales FontAwesome to 640 units per em so the
icons fill the em, and runs lv_font_conv for both fonts.

Sources:
  Montserrat  - https://github.com/google/fonts/tree/main/ofl/montserrat (SIL OFL 1.1)
  FontAwesome - https://github.com/FortAwesome/Font-Awesome (icons: CC BY 4.0, fonts: SIL OFL 1.1)

The generated C files are committed so normal firmware builds need no font
converter and no network access.
