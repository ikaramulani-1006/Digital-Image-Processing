import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

img = Image.open(r"C:\Users\Student\Desktop\research papers\Cat.jpg").convert("L")
img = np.array(img)

def Sampling(img, factor):
    sample = img[::factor, ::factor]
    return sample

def Quantization(img, bits):
    level = 2**bits
    step = 256/level
    quantized = np.floor(img/step)*step
    quantized = quantized.astype(np.uint8)
    return quantized


plt.figure(figsize = (14,8))     #Describe figure size
im_array = [img, Sampling(img,2), Sampling(img,4), Quantization(img, 8), Quantization(img, 4), Quantization(img, 2)]
title = ["Original", "Sampling Factor = 2", "Sampling Factor = 4", "8-bit Quantization","4-bit Quantization","2-bit Quantization" ]

for idx in range(6):
    #It creates and selects the first subplot within a grid that contains 2 rows and 3 columns
    plt.subplot(2,3,idx + 1)
    plt.imshow(im_array[idx],cmap='gray') 
    plt.title(title[idx])
    plt.axis('off')

plt.tight_layout()
plt.show()
