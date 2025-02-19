import torch
import numpy as np
from PIL import Image
from .dialog_generator_v2 import create_dialog_image, overlay_dialog_on_background

class CreateDialogImageV2:
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "create_dialog_image"
    CATEGORY = "text"
    DESCRIPTION = "Creates a customizable dialog box image with a name label and configurable styling options."

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "label_content": ("STRING", {"default": "Dr. Aeda"}),
                "label_enabled": ([True, False], {"default": True}),
                "label_position": (["left", "right"], {"default": "right"}),
                "label_font_size": ("INT", {"default": 28, "min": 8, "max": 64, "step": 1}),
                "label_font_color": ("STRING", {"default": "#C71585"}),
                "label_width": ("INT", {"default": 180, "min": 50, "max": 4096, "step": 10}),

                "dialog_content": ("STRING", {"default": "The quick brown fox jumped over the lazy dogs. Lorem ipsum dolor sit amet, consectetur adipiscing elit.", "multiline": True}),
                "dialog_bkg_color": ("STRING", {"default": "rgba(255, 105, 180, 0.5)"}),
                "dialog_font_color": ("STRING", {"default": "white"}),
                "dialog_font_size": ("INT", {"default": 26, "min": 8, "max": 64, "step": 1}),
                "dialog_border_color": ("STRING", {"default": "white"}),
                "dialog_border_width": ("INT", {"default": 6, "min": 1, "max": 20, "step": 1}),
                
                "dialog_position": (["top", "bottom"], {"default": "bottom"}),
                "dialog_alignment": (["left", "center", "right"], {"default": "center"}),
                "dialog_optimize": ([True, False], {"default": True}),
                
                "font_family": ("STRING", {"default": "Noto Color Emoji"}),
                "image_width": ("INT", {"default": 840, "min": 16, "max": 4096, "step": 1}),
                "image_height": ("INT", {"default": 210, "min": 16, "max": 4096, "step": 1}),
                
                "background_image": ("IMAGE", )
            }
        }

    def create_dialog_image(self, label_content, label_enabled, label_position, label_font_size, label_font_color, label_width,
                            dialog_content, dialog_bkg_color, dialog_font_color, dialog_font_size, 
                            dialog_border_color, dialog_border_width, dialog_position, dialog_alignment, dialog_optimize,
                            font_family, image_width, image_height, background_image):
        
        dialog_img = create_dialog_image(
            label_enabled, label_content, label_font_color, label_font_size, label_position,
            dialog_content, dialog_bkg_color, dialog_font_color, dialog_font_size, 
            dialog_border_color, dialog_border_width, font_family, image_width, image_height, dialog_alignment, label_width
        )

        # Check if background_image is a valid tensor (i.e., not empty)
        if background_image is not None and background_image.nelement() > 0:
            bg_np = (background_image.squeeze(0).cpu().numpy() * 255).astype(np.uint8)  # Convert tensor to numpy image
            bg_image = Image.fromarray(bg_np)  # Convert to PIL image
            
            composite_img = overlay_dialog_on_background(dialog_img, bg_image, dialog_position, dialog_alignment, dialog_optimize, image_width, image_height)
            final_img = composite_img
        else:
            final_img = dialog_img

        # Convert image to torch tensor
        image_np = np.array(final_img).astype(np.float32) / 255.0
        image_tensor = torch.from_numpy(image_np)[None, ...]
        return (image_tensor,)

NODE_CLASS_MAPPINGS = {
    "CreateDialogImageV2": CreateDialogImageV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CreateDialogImageV2": "Create Dialog Image V2"
}
