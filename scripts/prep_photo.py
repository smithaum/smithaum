from rembg import remove
from PIL import Image
import cv2
import numpy as np
import sys

# Input image name
input_path = "photo.jpg"
output_path = "source-prepped.png"

# Remove background
input_image = Image.open(input_path)
output = remove(input_image)

# Convert to OpenCV image
image = np.array(output)
image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)

# White background
background = np.ones((image.shape[0], image.shape[1], 3), dtype=np.uint8) * 255

alpha = image[:, :, 3] / 255.0

for c in range(3):
    background[:, :, c] = (
        alpha * image[:, :, c] + (1 - alpha) * background[:, :, c]
    )

# Convert to grayscale
gray = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)

# Improve contrast
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
gray = clahe.apply(gray)

# Save image
cv2.imwrite(output_path, gray)

print("Image saved as source-prepped.png")