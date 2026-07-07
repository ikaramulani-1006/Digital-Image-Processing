%pip install opencv-python
pip install matplotlib

import cv2
import matplotlib.pyplot as plt

img = cv2.imread(r"C:\Users\Student\Desktop\an-orange-kitten-sitting-on-a-blanket-photo.jpeg")

if img is None:
    print("Error: Image Not found!!!")
else:
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img_rgb)
    plt.axis("Off")
    plt.show()
