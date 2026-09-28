import re

with open("custom_right.keymap", "r") as f:
    content = f.read()

# Replace the row 4 bindings in all layers to map the right thumb keys to both col 0..2 and 3..5
# and change the right knob click to C_PP.
content = re.sub(
    r"(&kp SPACE  &lt 2 LS\(COMMA\)  &kp DEL    )&none      &none      &none      (&kp C_MUTE)",
    r"\1&kp DEL    &lt 2 LS(COMMA) &kp SPACE \2",
    content
)

# And for layers where right thumb cluster is `&none      &none            &kp DEL    &none      &none      &none      &kp C_MUTE`
content = re.sub(
    r"(&none      &none            &kp DEL    )&none      &none      &none      (&kp C_MUTE)",
    r"\1&kp DEL    &none            &none     \2",
    content
)
content = re.sub(
    r"(&tog 4     &trans           &trans     )&none      &none      &none      (&kp C_MUTE)",
    r"\1&trans     &trans           &tog 4    \2",
    content
)

# Update the right knob click to C_PP (it's the last C_MUTE on the line)
# Wait, actually let's just make the right knob C_PP explicitly in all of them
content = re.sub(
    r"(&kp C_MUTE)$",
    r"&kp C_PP",
    content,
    flags=re.MULTILINE
)

# Add the right encoder to sensor-bindings
# If it's C_VOL_UP C_VOL_DN, add Brightness
content = re.sub(
    r"sensor-bindings = <&inc_dec_kp C_VOL_UP C_VOL_DN>;",
    r"sensor-bindings = <&inc_dec_kp C_VOL_UP C_VOL_DN>, <&inc_dec_kp C_BRI_UP C_BRI_DN>;",
    content
)

# If it's C_BRI_UP C_BRI_DN, add Volume
content = re.sub(
    r"sensor-bindings = <&inc_dec_kp C_BRI_UP C_BRI_DN>;",
    r"sensor-bindings = <&inc_dec_kp C_BRI_UP C_BRI_DN>, <&inc_dec_kp C_VOL_UP C_VOL_DN>;",
    content
)

with open("custom_right.keymap", "w") as f:
    f.write(content)

with open("custom_left.keymap", "w") as f:
    f.write(content)

