import numpy as np 
image = np.array([[10, 20, 30, 40, 50], 
                 [15, 25, 35, 45, 55],
                 [20, 30, 40, 50, 60],
                 [25, 35, 45, 55, 65],
                 [30, 40, 50, 60, 70]])
print('Image Matrix:')
print(image)

x,y = 2,2    # center pixels
print('Selected Pixels: ')
print(f'Position = {x}, { y}')
print(f'value = {image[x, y]}')

N4 = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
ND = [(x-1, y-1), (x-1, y+1), (x+1, y-1), (x+1, y+1)]
N8 = N4 + ND
Nm = [pixel for pixel in N4 if pixel not in ND]

print(f'N4 (4-Neighbors): {N4}')
print(f'N4 Values: {[image[r, c] for r, c in N4]}\n')

print(f'ND (Diagonal Neighbors): {ND}')
print(f'ND Values: {[image[r, c] for r, c in ND]}\n')

print(f'N8 (8-Neighbors): {N8}')
print(f'N8 Values: {[image[r, c] for r, c in N8]}\n')

print(f'Nm (Difference N4 - ND): {Nm}')
print(f'Nm Values: {[image[r, c] for r, c in Nm]}\n')
