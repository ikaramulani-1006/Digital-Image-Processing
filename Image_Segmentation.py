import cv2
import math
import numpy as np

p = np.array([[40, 45, 48, 50, 42], [43, 46, 52, 49, 45], [44, 47, 180, 190, 175], [46, 50, 185, 200, 178], [100, 48, 170, 195, 182] ], dtype=np.uint8)

def Global_Manual(p):
    t = int(input("Enter Threshold Value: "))
    output = np.zeros(p.shape, dtype=np.uint8)
    rows, cols = p.shape
    for i in range(rows):
        for j in range(cols):
            if p[i][j] >= t:
                output[i][j] = 255
            else:
                output[i][j] = 0
    print("Threshold =", t)
    print(output)
    return output

def Global_Otsu(p):
    hist = np.zeros(256)
    rows, cols = p.shape
    n = rows * cols
    for i in range(rows):
        for j in range(cols):
            value = int(p[i][j])
            hist[value] = hist[value] + 1
    max_sig_B = -1
    best_t = 0
    for t in range(255):
        n0 = 0
        n1 = 0
        sum0 = 0
        sum1 = 0
        for i in range(t + 1):
            n0 = n0 + hist[i]
            sum0 = sum0 + i * hist[i]
        for i in range(t + 1, 256):
            n1 = n1 + hist[i]
            sum1 = sum1 + i * hist[i]
        if n0 == 0 or n1 == 0:
            continue

        w0 = n0 / n
        w1 = n1 / n

        u0 = sum0 / n0
        u1 = sum1 / n1

        mu = (u0 - u1) * (u0 - u1)
        sig_B = w0 * w1 * mu

        if sig_B > max_sig_B:
            max_sig_B = sig_B
            best_t = t

    output = np.zeros(p.shape, dtype=np.uint8)
    for i in range(rows):
        for j in range(cols):
            if p[i][j] >= best_t:
                output[i][j] = 255
            else:
                output[i][j] = 0

    print("Best Otsu Threshold =", best_t)
    print("Maximum Sigma B =", max_sig_B)
    print(output)
    return output

def Iterative_Threshold(p):
    rows, cols = p.shape
    total = 0
    for i in range(rows):
        for j in range(cols):
            total = total + int(p[i][j])
    told = total / (rows * cols)

    E = float(input("Enter Tolerance E: "))
    while True:
        sum0 = 0
        sum1 = 0
        count0 = 0
        count1 = 0
        for i in range(rows):
            for j in range(cols):
                if p[i][j] < told:
                    sum0 = sum0 + int(p[i][j])
                    count0 = count0 + 1
                else:
                    sum1 = sum1 + int(p[i][j])
                    count1 = count1 + 1

        if count0 == 0 or count1 == 0:            #done to avoid division by zero
            break

        u0 = sum0 / count0
        u1 = sum1 / count1

        tnew = (u0 + u1) / 2
        
        difference = tnew - told
        if difference < 0:
            difference = -difference
        if difference < E:
            told = tnew
            break

        told = tnew
    output = np.zeros(p.shape, dtype=np.uint8)
    for i in range(rows):
        for j in range(cols):
            if p[i][j] >= told:
                output[i][j] = 255
            else:
                output[i][j] = 0

    print("Final Iterative Threshold =", told)
    print(output)
    return output

def Adaptive_Mean(p):
    block = int(input("Enter Odd Block Size: "))
    c = float(input("Enter C: "))
    if block % 2 == 0:
        block = block + 1
    rows, cols = p.shape
    r = block // 2
    output = np.zeros(p.shape, dtype=np.uint8)
    for x in range(rows):
        for y in range(cols):
            total = 0
            count = 0
            for i in range(x - r, x + r + 1):
                for j in range(y - r, y + r + 1):
                    if i >= 0 and i < rows and j >= 0 and j < cols:
                        total = total + int(p[i][j])
                        count = count + 1
            mean = total / count
            t = mean - c
            
            if p[x][y] >= t:
                output[x][y] = 255
            else:
                output[x][y] = 0
    print(output)
    return output

def Adaptive_Gaussian(p):
    block = int(input("Enter Odd Block Size: "))
    c = float(input("Enter C: "))
    if block % 2 == 0:
        block = block + 1
    rows, cols = p.shape
    r = block // 2
    output = np.zeros(p.shape, dtype=np.uint8)
    sigma = block / 6
    for x in range(rows):
        for y in range(cols):
            weighted_sum = 0
            weight_total = 0
            for i in range(x - r, x + r + 1):
                for j in range(y - r, y + r + 1):
                    if i >= 0 and i < rows and j >= 0 and j < cols:
                        dx = i - x
                        dy = j - y
                        # Gaussian formula
                        exponent = -((dx * dx) + (dy * dy)) / (2 * sigma * sigma)
                        weight = math.exp(exponent)
                
                        weighted_sum = (weighted_sum + weight * int(p[i][j]) )
                        weight_total = weight_total + weight
            mean = weighted_sum / weight_total
            t = mean - c

            if p[x][y] >= t:
                output[x][y] = 255
            else:
                output[x][y] = 0
    print(output)
    return output

def Niblack(p):
    block = int(input("Enter Odd Block Size: "))
    k = float(input("Enter k: "))
    if block % 2 == 0:
        block = block + 1
    rows, cols = p.shape
    r = block // 2
    output = np.zeros(p.shape, dtype=np.uint8)
    for x in range(rows):
        for y in range(cols):
            values = []
            for i in range(x - r, x + r + 1):     # It stores local values
                for j in range(y - r, y + r + 1):
                    if i >= 0 and i < rows and j >= 0 and j < cols:
                        values.append(float(p[i][j]))
            total = 0
            for value in values:
                total = total + value
            mean = total / len(values)
            variance = 0
            for value in values:
                difference = value - mean
                variance = (variance + difference * difference)
            variance = variance / len(values)
            std = math.sqrt(variance)
            
            t = mean + k * std

            if p[x][y] >= t:
                output[x][y] = 255
            else:
                output[x][y] = 0
    print(output)
    return output

def Sauvola(p):
    block = int(input("Enter Odd Block Size: "))
    k = float(input("Enter k: "))
    R = float(input("Enter R: "))

    if block % 2 == 0:
        block = block + 1
    rows, cols = p.shape
    r = block // 2
    output = np.zeros(p.shape, dtype=np.uint8)
    for x in range(rows):
        for y in range(cols):
            values = []
            for i in range(x - r, x + r + 1):
                for j in range(y - r, y + r + 1):
                    if i >= 0 and i < rows and j >= 0 and j < cols:
                        values.append(float(p[i][j]))
            total = 0
            for value in values:
                total = total + value
            mean = total / len(values)
            variance = 0
            for value in values:
                difference = value - mean
                variance = (variance + difference * difference)
            variance = variance / len(values)
            std = math.sqrt(variance)

            t = mean * (1 + k * (std / R - 1))

            if p[x][y] >= t:
                output[x][y] = 255
            else:
                output[x][y] = 0
    print(output)
    return output

def Watershed_R_Growing(p):
    rows, cols = p.shape
    seed_x = int(input("Enter Seed Row: "))
    seed_y = int(input("Enter Seed Column: "))

    T = float(input("Enter Similarity Threshold: "))
    output = np.zeros(p.shape, dtype=np.uint8)

    if seed_x < 0 or seed_x >= rows or seed_y < 0 or seed_y >= cols:
        print("Invalid Seed Point")
        return output

    seed_value = int(p[seed_x][seed_y])

    stack = []
    stack.append([seed_x, seed_y])

    output[seed_x][seed_y] = 255
    while len(stack) > 0:
        current = stack.pop()
        x = current[0]
        y = current[1]

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                nx = x + dx
                ny = y + dy

                if (nx >= 0 and nx < rows and ny >= 0 and ny < cols):
                    if output[nx][ny] == 0:
                        difference = (int(p[nx][ny]) - seed_value)
                        if difference < 0:
                            difference = -difference
                        if difference <= T:
                            output[nx][ny] = 255
                            stack.append([nx, ny])
    print("Seed Value =", seed_value)
    print("Region Growing Result:")
    print(output)
    return output


def Watershed_R_Splitting(p):
    rows, cols = p.shape
    T = float(input("Enter Variance Threshold: "))
    output = np.zeros(p.shape, dtype=np.uint8)

    def split_region(start_row, end_row, start_col, end_col):
        region_rows = end_row - start_row
        region_cols = end_col - start_col

        if region_rows <= 0 or region_cols <= 0:
            return
        total = 0
        count = 0
        for i in range(start_row, end_row):
            for j in range(start_col, end_col):
                total = total + int(p[i][j])
                count = count + 1
        mean = total / count
        variance = 0
        for i in range(start_row, end_row):
            for j in range(start_col, end_col):
                difference = int(p[i][j]) - mean
                variance = (variance + difference * difference)
        variance = variance / count
        if variance <= T:
            for i in range(start_row, end_row):
                for j in range(start_col, end_col):
                    output[i][j] = 255
            return
        if region_rows <= 1 or region_cols <= 1:
            return

        mid_row = (start_row + end_row) // 2
        mid_col = (start_col + end_col) // 2

        split_region(start_row,mid_row,start_col,mid_col)
        split_region(start_row,mid_row,mid_col,end_col    )
        split_region(mid_row,end_row,start_col,mid_col)
        split_region(mid_row,end_row,mid_col,end_col)
        
    split_region(0,rows,0,cols)
    print("Region Splitting Result:")
    print(output)
    return output

    
while True:
    print("\nImage Segmentation Techniques: ")
    print("1. Global Manual Thresholding")
    print("2. Otsu Thresholding")
    print("3. Iterative Thresholding")
    print("4. Adaptive Mean Thresholding")
    print("5. Adaptive Gaussian Thresholding")
    print("6. Niblack Thresholding")
    print("7. Sauvola Thresholding")
    print("8. Watershed Segmentation -  Region Growing ")
    print("9. Watershed Segmentation -  Region Splitting ")
    print("0. Exit")

    choice = int(input("Enter Choice: "))
    if choice == 1:
        Global_Manual(p)
    elif choice == 2:
        Global_Otsu(p)
    elif choice == 3:
        Iterative_Threshold(p)
    elif choice == 4:
        Adaptive_Mean(p)
    elif choice == 5:
        Adaptive_Gaussian(p)
    elif choice == 6:
        Niblack(p)
    elif choice == 7:
        Sauvola(p)
    elif choice == 8:
        Watershed_R_Growing(p)
    elif choice == 9:
            Watershed_R_Splitting(p)
    elif choice == 0:
        print("Program Ended")
        break
    else:
        print("Invalid Choice")