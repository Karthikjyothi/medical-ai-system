import cv2
from utils.gradcam import generate_gradcam

output = generate_gradcam("test.jpg")

cv2.imwrite("gradcam_output.jpg", output)
print("Grad-CAM saved as gradcam_output.jpg")