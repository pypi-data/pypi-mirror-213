import numpy as np
from skimage.io import imread, imsave
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageIO:

    @staticmethod
    def read_image(image_path):
        """
        Reads an image from the specified path.

        :param image_path: Path to image.
        :type image_path: str
        :return: Image as a numpy array.
        :rtype: numpy.ndarray
        """
        try:
            image = imread(image_path)
            logger.info("Image read from %s", image_path)
            return image
        except FileNotFoundError:
            logger.error("File not found at %s", image_path)
            raise


    @staticmethod
    def save_image(image, path):
        """
        Saves an image to the specified path.

        :param image: Image to be saved.
        :type image: numpy.ndarray
        :param path: Path to save image.
        :type path: str
        """
        try:
            imsave(path, image)
            logger.info("Image saved to %s", path)
        except:
            logger.error("Error saving image to %s", path)
            raise

