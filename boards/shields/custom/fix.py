with open("custom_right.keymap", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "C_MUTE" in line and "RC(3,13)" not in line:
        pass
    if line.strip().startswith("&none     &none    &none"):
        # This is a bottom row.
        # Original from memory:
        # &none     &none    &none    &kp LALT   &lt 2 EXCL &mt LGUI SPACE &kp C_MUTE &kp SPACE  &lt 2 LS(COMMA)  &kp DEL    &none      &none      &none      &kp C_MUTE
        pass
