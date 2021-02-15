import sys
import numpy as np
from imageio import imread, imwrite
from scipy.ndimage.filters import convolve

def calc_energy(img):
    filter_du = np.array([
         [1.0, 2.0, 1.0],
        [0.0, 0.0, 0.0],
        [-1.0, -2.0, -1.0],
    ])
    filter_du = np.stack([filter_du]*3, axis=2)

    filter_dv = np.array([
        [1.0, 0.0, -1.0],
        [2.0, 0.0, -2.0],
        [1.0, 0.0, -1.0],
    ])
    filter_dv = np.stack([filter_dv] * 3, axis=2)

    img = img.astype('float32')
    convolved = np.absolute(convolve(img, filter_du)) + np.absolute(convolve(img, filter_dv))
    energy_map = convolved.sum(axis=2)

    # for i in range(0, np.shape(energy_map)[0]):
    #     energy_map[i][0] = 100000000
    #     energy_map[i][np.shape(energy_map)[1]-1] = 100000000

    return energy_map

def find_minimal_seam(img):
    height = np.shape(img)[0]
    width = np.shape(img)[1]

    opt = [[100000000 for i in range(width)] for j in range(height)]
    act = [[100000000 for i in range(width)] for j in range(height)]

    for i in range(width):
        opt[0][i] = img[0][i]
    

    for i in range(1, height):
        for j in range(1, width-1):
            opt[i][j] = opt[i-1][j]
            act[i][j] = 0
            if opt[i-1][j-1] < opt[i][j]:
                opt[i][j] = opt[i-1][j-1]
                act[i][j] = -1
            if opt[i-1][j+1] < opt[i][j]:
                opt[i][j] = opt[i-1][j+1]
                act[i][j] = 1
            opt[i][j] += img[i][j]

    # print(img)
    # print(opt)
    # print(act)
    
    end = 1
    for i in range(1, width-1):
        if opt[height-1][i] < opt[height-1][end]:
            end = i
    
    # print(end)

    seam = []
    cur = end
    for i in range(height, 0, -1):
        seam.append(cur)
        cur += act[i-1][cur]
    seam.reverse()

    return seam


img = imread('inn.jpg')
out = calc_energy(img)
# print(find_minimal_seam(out))

width = np.shape(img)[1]
height = np.shape(img)[0]
print(np.shape(img))
img = img.tolist()
for i in range(200):
    seam = find_minimal_seam(out)
    j = 0
    for i in seam:
        # img = np.delete(img, j*width + i, None)
        del img[j][i]
        out = out.tolist()
        del out[j][i]
        out = np.array(out)
        # img[j][i] = [255,0,0]
        # out[j][i] = 10000
        j += 1
img = np.array(img)
print(np.shape(img))
imwrite('b.jpg', img)

# [[1000,4,6,2,5,7,3,6,1000],
#                             [4000,7,2,5,3,7,2,3,1000],
#                             [6000,3,7,2,4,5,3,5,1000],
#                             [2000,4,5,7,8,9,5,6,1000]   ]