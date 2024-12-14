from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageOps
import numpy as np
import cv2


class ImageProcessor:
    @staticmethod
    def load_image(file_path):
        try:
            return Image.open(file_path)
        except Exception as e:
            raise ValueError(f"Error loading image: {e}")

    @staticmethod
    def apply_grayscale(image):
        return image.convert('L')

    @staticmethod
    def apply_blur(image, radius=5):
        return image.filter(ImageFilter.GaussianBlur(radius))

    @staticmethod
    def detect_edges(image):
        img_array = np.array(image.convert('RGB'))
        edges = cv2.Canny(img_array, 100, 200)
        return Image.fromarray(edges)

    @staticmethod
    def adjust_brightness(image, factor=1.5):
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)

    @staticmethod
    def adjust_contrast(image,factor=1.5):
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)

    @staticmethod
    def adjust_sharpness(image, factor=2):
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(factor)

    @staticmethod
    def adjust_saturation(image, factor=1):
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(factor)

    @staticmethod
    def apply_hist_equalization(image):
        return ImageOps.equalize(image)

    @staticmethod
    def apply_padding(image,left=0,top=0,right=0,bottom=0,color=(0,0,0)):
        return ImageOps.expand(image,left,top,right,bottom,fill=color)