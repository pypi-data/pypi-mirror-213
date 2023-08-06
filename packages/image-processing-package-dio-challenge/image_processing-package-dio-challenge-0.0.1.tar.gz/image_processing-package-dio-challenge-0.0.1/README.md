# Image Processing Package

This package provides functionality for image processing and generate a normal map texture.

## Package: ImageIO

The `ImageIO` package is responsible for reading and saving images.

### Methods

- `read_image(image_path: str) -> numpy.ndarray`: Reads an image from the specified path and returns it as a NumPy array.

- `save_image(image: numpy.ndarray, path: str) -> None`: Saves an image to the specified path.

## Package: ImageProcessing

The `ImageProcessing` package is responsible for image processing and generating a normal map.

### Methods

- `generate_normal_map(image: numpy.ndarray) -> PIL.Image.Image`: Generates a normal map from an input image and returns it as a PIL Image object.

## Package: imagePlot

The `imagePlot` package is responsible for displaying and saving images.

### Methods

- `plot(image: numpy.ndarray) -> None`: Displays an image and saves it to the current directory.


## Usage

Here's an example of how to use the Image Processing Package:

```python
from ImageIO import ImageIO
from ImageProcessing import ImageProcessing
from imagePlot import Plot

# Read an image
image = ImageIO.read_image('path/to/image.jpg')

# Generate a normal map
normal_map = ImageProcessing.generate_normal_map(image)

# Save the normal map
ImageIO.save_image(normal_map, 'path/to/normal_map.png')

# Display and save the image
plotter = Plot()
plotter.plot(image)

```
## Requirements

The Image Processing Package has the following requirements:

numpy
opencv_python
Pillow
scikit-image