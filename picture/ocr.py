
import pytesseract
import os
import sys
import cv2
import numpy as np
from PIL import Image


def get_string(img_path):

	src_path, file_name = os.path.split(img_path)

	pic_removed_noise = src_path + "/removed_noise.png"
	pic_thres = src_path + "/thres.png"

	# Read image with opencv
	img = cv2.imread(img_path)
	# Convert to gray
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# Apply dilation and erosion to remove some noise
	kernel = np.ones((1, 1), np.uint8)
	img = cv2.dilate(img, kernel, iterations=1)
	img = cv2.erode(img, kernel, iterations=1)

	cv2.imwrite(pic_removed_noise, img)

	# Apply threshold to get image with only black and white
	img = cv2.adaptiveThreshold(
	    img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
	cv2.imwrite(pic_thres, img)

	# Recognize text with tesseract for python
	# chi_sim=Chinese eng=English
    # pytesseract.image_to_string(image.show(), lang='eng')
	result = pytesseract.image_to_string(Image.open(src_path + "/thres.png"))
	os.remove(pic_thres)
	os.remove(pic_removed_noise)
	return result


img_path = "C:/Users/it/Desktop/test.png"
if not os.path.exists(img_path):
	print("Please check your image path!")
	sys.exit()

print("--- Start recognize text")
print(get_string(img_path))
