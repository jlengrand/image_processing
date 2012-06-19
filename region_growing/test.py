import cv
 
import segmentations as se
import basic_operations as bo
import display_operations as do
 
user_input = 0
 
img_name = "data/gnu.jpg"
threshold = 20
img = cv.LoadImage(img_name, cv.CV_LOAD_IMAGE_GRAYSCALE)
 
if user_input:
    seed = bo.mouse_point(img, mode="S") # waits for user click to get seed
else:
    seed = (70, 106)
 
out_img = se.simple_region_growing(img, seed, threshold)
 
do.display_single_image(out_img, "Region Growing result")
