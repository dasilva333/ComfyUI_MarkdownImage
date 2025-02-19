#!/usr/bin/env python3
from io import BytesIO
from PIL import Image
import torch
import numpy as np
import markdown
import time
import urllib.parse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def create_dialog_image(label_enabled, label_content, label_font_color, label_font_size, label_position,
                          dialog_content, dialog_background, dialog_font_color, dialog_font_size, 
                          dialog_border_color, dialog_border_width, font_family, canvas_width, canvas_height, 
                          dialog_alignment, label_width):
    label_html = (
        f'<div class="name-label {"right-label" if label_position == "right" else "left-label"}">{label_content}</div>'
        if label_enabled else ""
    )
    dialog_html = markdown.markdown(dialog_content)
    styled_html = f"""
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            background: transparent;
            margin: 0;
            padding: 0;
            display: flex;
            align-items: center;
            justify-content: {dialog_alignment};
            height: 100%;
        }}
        p, span, div, h1, h2, h3, h4, h5, h6 {{
            margin: 0;
            padding: 0;
        }}
        .container {{
            width: {canvas_width}px;
            padding-top: 10px;
        }}
        .name-label {{
            display: flex;
            align-items: center;
            background: white;
            color: {label_font_color};
            font-family: '{font_family}', sans-serif;
            font-size: {label_font_size}px;
            font-weight: bold;
            padding: 8px 16px;
            border-radius: 10px 10px 0 0;
            width: {label_width}px;
        }}
        .left-label {{
            margin-left: 12px;
        }}
        .right-label {{
            margin-left: auto;
            margin-right: 12px;
            justify-content: flex-end;
        }}
        .dialog-box {{
            width: 100%;
            background: {dialog_background};
            border: {dialog_border_width}px solid {dialog_border_color};
            border-radius: 12px;
            padding: 30px;
            box-sizing: border-box;
            font-family: '{font_family}', sans-serif;
            color: {dialog_font_color};
            font-size: {dialog_font_size}px;
            line-height: 1.4;
            text-align: left;
        }}
    </style>
</head>
<body>
    <div class="container">
        {label_html}
        <div class="dialog-box">{dialog_html}</div>
    </div>
</body>
</html>
"""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size={}x{}".format(canvas_width, canvas_height))
    options.add_argument("--hide-scrollbars")
    options.add_argument("--window-position=-10000,-10000")
    
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd(
        "Emulation.setDefaultBackgroundColorOverride",
        {"color": {"r": 0, "g": 0, "b": 0, "a": 0}}
    )
    html_data = "data:text/html;charset=utf-8," + urllib.parse.quote(styled_html)
    driver.get(html_data)
    time.sleep(2)
    screenshot = driver.get_screenshot_as_png()
    driver.quit()
    
    with Image.open(BytesIO(screenshot)).convert("RGBA") as img:
        dialog_img = img.crop((0, 3, img.width, img.height))
    return dialog_img

def overlay_dialog_on_background(dialog_img, background_image, dialog_position, dialog_alignment, dialog_optimize, canvas_width, canvas_height):
    if isinstance(background_image, torch.Tensor):
        bg_np = (background_image.squeeze(0).cpu().numpy() * 255).astype(np.uint8)
        background = Image.fromarray(bg_np).convert("RGBA")
    elif isinstance(background_image, Image.Image):
        background = background_image.convert("RGBA")
    else:
        raise ValueError("Invalid background_image type. Expected a torch.Tensor or PIL.Image.")

    bg_width, bg_height = background.size
    empty_bottom_margin = 0
    
    if dialog_position == "bottom" and dialog_optimize:
        bbox = dialog_img.getbbox()
        if bbox:
            empty_bottom_margin = canvas_height - bbox[3] - 10

    y_position = 0 if dialog_position == "top" else (
        bg_height - canvas_height + empty_bottom_margin if dialog_optimize else bg_height - canvas_height
    )
    if dialog_alignment == "left":
        x_position = 0
    elif dialog_alignment == "center":
        x_position = (bg_width - canvas_width) // 2
    else:
        x_position = bg_width - canvas_width

    background.paste(dialog_img, (x_position, y_position), dialog_img)
    return background
