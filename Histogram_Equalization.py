import numpy as np
import matplotlib.pyplot as plt

gray_levels = np.array([0,1,2,3,4,5,6,7])
pixels = np.array([9,8,11,4,10,15,4,3])

N = np.sum(pixels)
L = len(gray_levels)
pdf = pixels / N

cdf = []
sum_pdf = 0
for i in pdf:
    sum_pdf += i
    cdf.append(sum_pdf)
cdf = np.array(cdf)

Sk = cdf  * 7
Sk = np.array(Sk)

Histogram_levels = np.round((L - 1) * cdf).astype(int)

equalized = np.zeros(L)
for i in range(L):
    equalized[Histogram_levels[i]] += pixels[i] 
    
print("GrayLevel  Pixels   PDF           CDF       Sk*7     Histogram Level")
for i in range(L):
    print(f"{gray_levels[i]}           {pixels[i]}\t   {pdf[i]:.4f}\t{cdf[i]:.4f}    {Sk[i]:.4f}\t   {Histogram_levels[i]}")

print("Gray levels:", Histogram_levels)
print("No. of Pixels:", pixels)
plt.hist(Histogram_levels, bins= range(L+1 ), color='pink', edgecolor='black', weights = pixels)
plt.ylabel('No. of Pixels')
plt.xlabel('Gray levels')
plt.title('Histogram Equalization')
plt.show()
