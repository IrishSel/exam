import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import filters
from skimage.measure import label, regionprops


image = plt.imread('task1.png')
image1 = np.mean(image, 2)

sobel = filters.sobel(image1)
sobel = np.array(sobel)
sobel[sobel > 0] = 1

labeled = label(sobel)

regions = regionprops(labeled)

images = []
areas = []
for region in regions:
    if not np.all(region.image):
        area = 0
        beginning = False
        in_figure = False
        for i in range(region.image.shape[0]):
            for j in range(region.image.shape[1] - 1):
                if beginning:
                    if in_figure:
                        if region.image[i][j] == 0:
                            area += 1
                        else:
                            in_figure = False
                    else:
                        if region.image[i][j] == 1 and region.image[i][j + 1] == 0:
                            in_figure = True
                elif region.image[i][j] == 0 and region.image[i - 1][j] == 1 and region.image[i][j - 1] == 1:
                    beginning = True
                    in_figure = True
        images.append(region.image)
        areas.append(area)

max_area = [0, 0]
for area_ind in range(len(areas)):
    if areas[area_ind] > max_area[0]:
        max_area = [areas[area_ind], area_ind]

print('Максимальная внутренняя площадь', max_area[0])
plt.figure()
plt.imshow(images[max_area[1]])

print('Все площади:', areas)

plt.figure()
plt.subplot(121)
plt.imshow(image)
plt.subplot(122)
plt.imshow(labeled)
plt.show()