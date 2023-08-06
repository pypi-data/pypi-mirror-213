import numpy as np
from PIL import Image
import cv2
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageProcessing:
    """
    A class for processing images.
    """

    @staticmethod
    def generate_normal_map(image):
        """
        Generates a normal map from an input image.

        :param image: Input image.
        :type image: numpy.ndarray
        :return: Normal map image.
        :rtype: PIL.Image.Image
        """
        try:
            # Convert image to float32 and normalize pixel values
            image = image.astype(np.float32) / 255.0 
            
            # Get image dimensions
            height, width, _ = image.shape

            # Initialize normal map with zeros
            normal_map = np.zeros((height, width, 3), dtype=np.uint8)

            # Calculate partial derivatives using Sobel filter
            gradient_x = cv2.Sobel(image, cv2.CV_32F, 1, 0, ksize=3)
            gradient_y = cv2.Sobel(image, cv2.CV_32F, 0, 1, ksize=3)

            # Calculate X, Y, and Z components of normal vector
            normal_map[..., 0] = np.rint((gradient_x[..., 0] + 1) * 0.5 * 255)
            normal_map[..., 1] = np.rint((gradient_y[..., 1] + 1) * 0.5 * 255)
            normal_map[..., 2] = np.rint(255.0 / np.sqrt(1 + np.square(gradient_x[..., 0]) + np.square(gradient_y[..., 1])))

            # Convert normal map to PIL image
            normal_map_image = Image.fromarray(normal_map)

            # Log success message
            logger.info("Normal map generated successfully.")

            return normal_map_image

        except Exception as e:
            # Log error message
            logger.error("Error generating normal map: %s", str(e))
            raise e
