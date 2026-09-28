with open("custom.dtsi", "r") as f:
    text = f.read()

import re

# Remove the incorrectly placed encoder block
bad_block = r"""
    left_encoder: encoder_left \{
        compatible = "alps,ec11";
        a-gpios = <&gpio1 15 \(GPIO_ACTIVE_HIGH \| GPIO_PULL_UP\)>;
        b-gpios = <&gpio1 13 \(GPIO_ACTIVE_HIGH \| GPIO_PULL_UP\)>;
        steps = <80>;
        status = "disabled";
    \};

    right_encoder: encoder_right \{
        compatible = "alps,ec11";
        a-gpios = <&gpio0 6 \(GPIO_ACTIVE_HIGH \| GPIO_PULL_UP\)>;
        b-gpios = <&gpio0 8 \(GPIO_ACTIVE_HIGH \| GPIO_PULL_UP\)>;
        steps = <80>;
        status = "disabled";
    \};

    sensors: sensors \{
        compatible = "zmk,keymap-sensors";
        sensors = <&left_encoder &right_encoder>;
        triggers-per-rotation = <20>;
    \};"""

text = re.sub(bad_block, "", text)

encoders = """
    left_encoder: encoder_left {
        compatible = "alps,ec11";
        a-gpios = <&gpio1 15 (GPIO_ACTIVE_HIGH | GPIO_PULL_UP)>;
        b-gpios = <&gpio1 13 (GPIO_ACTIVE_HIGH | GPIO_PULL_UP)>;
        steps = <80>;
        status = "disabled";
    };

    right_encoder: encoder_right {
        compatible = "alps,ec11";
        a-gpios = <&gpio0 6 (GPIO_ACTIVE_HIGH | GPIO_PULL_UP)>;
        b-gpios = <&gpio0 8 (GPIO_ACTIVE_HIGH | GPIO_PULL_UP)>;
        steps = <80>;
        status = "disabled";
    };

    sensors: sensors {
        compatible = "zmk,keymap-sensors";
        sensors = <&left_encoder &right_encoder>;
        triggers-per-rotation = <20>;
    };
"""

# Insert correctly into the root node
text = text.replace("default_transform: keymap_transform_0 {", encoders + "\n    default_transform: keymap_transform_0 {")

with open("custom.dtsi", "w") as f:
    f.write(text)

