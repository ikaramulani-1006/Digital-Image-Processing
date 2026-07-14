import numpy as np

image = np.array([[10, 20, 30, 40, 50],
                  [15, 25, 35, 45, 55],
                  [20, 30, 40, 50, 60],
                  [25, 35, 45, 55, 65],
                  [30, 40, 50, 60, 70]])

print("Image Matrix:\n")
print(image)

x, y = 2, 2

print("\nSelected Pixel:")
print(f"Position = ({x}, {y})")
print(f"Value = {image[x, y]}")


N4 = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

ND = [(x-1, y-1), (x-1, y+1),
      (x+1, y-1), (x+1, y+1)]

N8 = N4 + ND

print("\n4-Neighbors:")
for i, j in N4:
    print(f"({i}, {j}) = {image[i, j]}")

print("\nDiagonal Neighbors:")
for i, j in ND:
    print(f"({i}, {j}) = {image[i, j]}")

print("\n8-Neighbors:")
for i, j in N8:
    print(f"({i}, {j}) = {image[i, j]}")

Nm = []
for p in N4:
    if p not in ND:
        Nm.append(p)
        
print('\nM-neighbours (Difference N4 - ND)')
for i, j in ND:
    print(f"({i}, {j}) = {image[i, j]}")
