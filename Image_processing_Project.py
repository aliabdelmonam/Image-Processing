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
    def apply_padding(image,left=0,top=0,right=0,bottom=0,fill=None):
        if fill is None:
            fill = (0, 0, 0)
        padded_img = ImageOps.expand(image, (left, top, right, bottom), fill=fill)
        return padded_img

    @staticmethod
    def apply_blur(image, radius=5):
        return image.filter(ImageFilter.GaussianBlur(radius))

    @staticmethod
    def apply_median_filter(image, size=1):
        return image.filter(ImageFilter.MedianFilter(size=size))

    @staticmethod
    def apply_bilateral_filter(image,d=1 ,sigmacolor=1, sigmaspace=1):
        # Convert PIL image to OpenCV format
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        filtered = cv2.bilateralFilter(cv_image, d=d, sigmaColor=sigmacolor, sigmaSpace=sigmaspace)
        # Convert back to PIL image
        return Image.fromarray(cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB))

    @staticmethod
    def apply_transformation(image,angle=0,scale=1):
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        height, width = cv_image.shape[:2]

        # Define the center of rotation
        center = (width / 2, height / 2)

        rotation_matrix = cv2.getRotationMatrix2D(center=center, angle=angle, scale=scale)

        # Step 2: Apply the rotation using warpAffine
        rotated_image = cv2.warpAffine(cv_image, rotation_matrix, (width, height))

        return Image.fromarray(cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB))

