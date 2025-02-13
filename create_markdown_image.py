# create_markdown_image.py
import markdown
import imgkit
import numpy as np
import torch
from PIL import Image
from io import BytesIO

class CreateMarkdownImage:
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "createmarkdownimage"
    CATEGORY = "text"
    DESCRIPTION = (
        "Creates an image from markdown text using imgkit. "
        "The text is auto-scaled to fit within the container."
    )

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "md_text": (
                    "STRING",
                    {
                        "default": "<span style=\"color: #C71585;\"><b>Girl:</b></span> Do you think the bunnies are watching us? 🐰<br>\n<span style=\"color: #00008B;\"><b>Man:</b></span> Only to wish they could be as happy as we are. 😂",
                        "multiline": True,
                    },
                ),
                "border_color": ("STRING", {"default": "#FFFF00"}),
                "border_size": ("INT", {"default": 1, "min": 0, "max": 100, "step": 1}),
                "image_width": ("INT", {"default": 1024, "min": 16, "max": 4096, "step": 1}),
                "image_height": ("INT", {"default": 200, "min": 16, "max": 4096, "step": 1}),
                "background_color": ("STRING", {"default": "lightblue"}),
            }
        }

    def createmarkdownimage(self, md_text, border_color, border_size, image_width, image_height, background_color):
        html_content = markdown.markdown(md_text)
        styled_html = f"""
<html>
<head>
    <style>
        html, body {{
            margin: 0;
            padding: 0;
        }}
        p {{
            margin: 0;
            padding: 0;
        }}
        #container {{
            font-family: 'Segoe UI Emoji', sans-serif;
            background-color: {background_color};
            width: {image_width}px;
            height: {image_height}px;
            box-sizing: border-box;
            border: {border_size}px solid {border_color};
            display: flex;
            justify-content: flex-start;
            align-items: flex-start;
            text-align: center;
            overflow: hidden;
        }}
        #text {{
            font-size: 1px;
            line-height: 1.2;
            white-space: nowrap;
            margin: 0;
            padding: 0;
        }}
    </style>
</head>
<body>
    <div id="container">
        <div id="text">{html_content}</div>
    </div>
    <script>
    function adjustFontSize() {{
        var container = document.getElementById('container');
        var text = document.getElementById('text');
        var low = 1, high = 1000, fontSize = 1;
        while (low <= high) {{
            var mid = Math.floor((low + high) / 2);
            text.style.fontSize = mid + 'px';
            if (
                text.scrollWidth <= container.clientWidth &&
                text.scrollHeight <= container.clientHeight
            ) {{
                fontSize = mid;
                low = mid + 1;
            }} else {{
                high = mid - 1;
            }}
        }}
        text.innerHTML = text.innerHTML.trim();
        text.style.fontSize = fontSize + 'px';
    }}
    window.onload = adjustFontSize;
    </script>
</body>
</html>
"""

        config = imgkit.config(wkhtmltoimage=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe")
        options = {
            'format': 'png',
            'width': image_width,
            'height': image_height,
            'encoding': "UTF-8"
        }
        image_bytes = imgkit.from_string(styled_html, False, options=options, config=config)
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        image_np = np.array(image).astype(np.float32) / 255.0
        image_tensor = torch.from_numpy(image_np)[None, ...]
        return (image_tensor,)

NODE_CLASS_MAPPINGS = {
    "CreateMarkdownImage": CreateMarkdownImage
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CreateMarkdownImage": "Create Markdown Image"
}
