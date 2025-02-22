import os
import urllib.parse
import time
import numpy as np
import torch
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class CreateMarkdownImageV2:
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "createmarkdownimage"
    CATEGORY = "text"
    DESCRIPTION = "Creates an image from an external HTML file using Chrome Driver with Selenium."

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
                "theme": (["pastel", "rose", "barbie", "preppy", "neutral-sky", "yellow-tan"], {"default": "pastel"}),
            }
        }

    def createmarkdownimage(
        self,
        md_text,
        border_color,
        border_size,
        image_width,
        image_height,
        theme,
    ):
        # Get absolute path of the local HTML file
        base_path = os.path.dirname(os.path.abspath(__file__))
        # print(base_path)
        # Create a dictionary of the input parameters
        query_params = {
            "md_text": md_text,
            "border_color": border_color,
            "border_size": border_size,
            "image_width": image_width,
            "image_height": image_height,
            "theme": theme,
        }

        # Encode the query string using urllib
        query_string = urllib.parse.urlencode(query_params)

        # Construct the full file path with query parameters
        html_path = f"file://{os.path.join(base_path, 'test5.html')}?{query_string}"
        # print(html_path) 
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--hide-scrollbars") 
        options.add_argument(f"--window-size={image_width},{image_height}")

        driver = webdriver.Chrome(options=options)

        # Force the exact viewport size
        driver.execute_cdp_cmd(
            "Emulation.setDeviceMetricsOverride",
            {
                "width": image_width,
                "height": image_height,
                "deviceScaleFactor": 1,
                "mobile": False
            }
        )

        # Load the external HTML file
        driver.get(html_path)
        time.sleep(5)  # Ensure styles and JS are applied

        # Capture a screenshot
        screenshot = driver.get_screenshot_as_png()
        driver.quit()

        # Convert to PyTorch tensor
        image = Image.open(BytesIO(screenshot)).convert("RGB")
        image_np = np.array(image).astype(np.float32) / 255.0
        image_tensor = torch.from_numpy(image_np)[None, ...]

        return (image_tensor,)

NODE_CLASS_MAPPINGS = {
    "CreateMarkdownImageV2": CreateMarkdownImageV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CreateMarkdownImageV2": "Create Markdown Image V2"
}
