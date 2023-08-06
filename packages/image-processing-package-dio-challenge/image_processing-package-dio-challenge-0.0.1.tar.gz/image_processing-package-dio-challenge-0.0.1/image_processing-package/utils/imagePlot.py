import cv2
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Plot:

    def plot(self, image):
        """
        Displays an image and saves it to the current directory.

        :param image: Image to be displayed and saved.
        :type image: numpy.ndarray
        """
        try:
            # Save image to current directory
            cv2.imwrite("image.png", image)
            
            # Display image
            cv2.imshow("Image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
            # Log success message
            logger.info("Image displayed and saved successfully.")
        except Exception as e:
            # Log error message
            logger.error("Error occurred while displaying and saving image: %s", str(e))