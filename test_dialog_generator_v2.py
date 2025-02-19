#!/usr/bin/env python3
from .dialog_generator_v2 import create_dialog_image, overlay_dialog_on_background
from PIL import Image

def main():
    label_enabled = True
    label_content = "User"
    label_font_color = "#000000"
    label_font_size = 24
    label_position = "left"
    dialog_content = "Hello, **World!** This is a test with new emojis 😵‍💫🪄🥱"
    dialog_background = "#F0F0F0"
    dialog_font_color = "#333333"
    dialog_font_size = 32
    dialog_border_color = "#FF0000"
    dialog_border_width = 2
    font_family = "Noto Color Emoji"
    canvas_width = 800
    canvas_height = 300
    dialog_alignment = "center"
    label_width = 200

    dialog_img = create_dialog_image(
        label_enabled, label_content, label_font_color, label_font_size, label_position,
        dialog_content, dialog_background, dialog_font_color, dialog_font_size,
        dialog_border_color, dialog_border_width, font_family, canvas_width, canvas_height,
        dialog_alignment, label_width
    )

    background = Image.new("RGBA", (1024, 768), "#CCCCCC")
    final_img = overlay_dialog_on_background(dialog_img, background, "bottom", dialog_alignment, True, canvas_width, canvas_height)
    
    final_img.save("output_dialog_v2.png")

if __name__ == "__main__":
    main()
