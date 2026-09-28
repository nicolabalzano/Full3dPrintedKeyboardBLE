import re
with open("custom_right.keymap", "r") as f:
    text = f.read()

# Fix accent layer
text = re.sub(
    r"(&kp SPACE  &kp LS\(COMMA\)    &kp DEL    )&none      &none      &none      (&kp C_PP)",
    r"\1&kp DEL    &kp LS(COMMA)    &kp SPACE \2",
    text
)
# Fix symbols layer
text = re.sub(
    r"(&kp N0     &trans           &kp DEL    )&none      &none      &none      (&kp C_PP)",
    r"\1&kp DEL    &trans           &kp N0    \2",
    text
)
with open("custom_right.keymap", "w") as f:
    f.write(text)

with open("custom_left.keymap", "w") as f:
    f.write(text)
