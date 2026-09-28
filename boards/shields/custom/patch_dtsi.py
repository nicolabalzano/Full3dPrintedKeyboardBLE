with open("custom.dtsi", "r") as f:
    dtsi = f.read()

if "left_encoder" not in dtsi:
    # Add encoders to custom.dtsi
    encoders_dtsi = """
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
    # Insert before the last brace
    dtsi = dtsi.replace("};", encoders_dtsi + "\n};", 1)
    
    with open("custom.dtsi", "w") as f:
        f.write(dtsi)

# Now remove the redundant nodes from custom_left.overlay and custom_right.overlay
def patch_overlay(file, encoder_node):
    with open(file, "r") as f:
        content = f.read()
    # Find the start of the encoder block
    import re
    content = re.sub(r"    [a-z_]+_encoder: encoder \{[\s\S]*?status = \"okay\";\n    \};\n", "", content)
    content = re.sub(r"    sensors \{[\s\S]*?triggers-per-rotation = <20>;\n    \};\n", "", content)
    
    # Enable the specific encoder
    content = content + f"\n&{encoder_node} {{\n    status = \"okay\";\n}};\n"
    with open(file, "w") as f:
        f.write(content)

patch_overlay("custom_left.overlay", "left_encoder")
patch_overlay("custom_right.overlay", "right_encoder")
