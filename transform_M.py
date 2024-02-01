"""
Python Image Manipulation Empty Template by Kylie Ying (modified from MIT 6.865)

YouTube Kylie Ying: https://www.youtube.com/ycubed 
Twitch KylieYing: https://www.twitch.tv/kylieying 
Twitter @kylieyying: https://twitter.com/kylieyying 
Instagram @kylieyying: https://www.instagram.com/kylieyying/ 
Website: https://www.kylieying.com
Github: https://www.github.com/kying18 
Programmer Beast Mode Spotify playlist: https://open.spotify.com/playlist/4Akns5EUb3gzmlXIdsJkPs?si=qGc4ubKRRYmPHAJAIrCxVQ 
"""

from image import Image
import numpy as np
import concurrent.futures as cf
from multiprocessing import cpu_count
from tqdm import tqdm
import psutil
from scipy.ndimage import median_filter, convolve


def brighten(image, factor):
    # when we brighten, we just want to make each channel higher by some amount 
    # factor is a value > 0, how much you want to brighten the image by (< 1 = darken, > 1 = brighten)
    x_pixels, y_pixels, num_channels = image.array.shape
    new_image = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)  

    new_image.array = image.array * factor
    return new_image

def adjust_contrast(image, factor, mid=0.5):
    # adjust the contrast by increasing the difference from the user-defined midpoint by factor amount
    x_pixels, y_pixels, num_channels = image.array.shape
    new_image = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)  

    new_image.array = (image.array - mid) * factor + mid

    return new_image 

def combine_images(image1, image2):

    # let's combine two images using the squared sum of squares: value = sqrt(value_1**2, value_2**2)
    # size of image1 and image2 MUST be the same
    x_pixels, y_pixels, num_channels = image1.array.shape
    new_image = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)  

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_image.array[x, y, c] = ((image1.array[x, y, c]**2) + (image2.array[x, y, c]**2))**0.5
    return new_image

def parse_image(image, func, kernel):
    x_all, y_all, num_all = image.array.shape
    new_image = Image(x_pixels=x_all, y_pixels=y_all, num_channels=num_all)
    cores_num = 9
    #psutil.cpu_count(logical=False)
    #  y_Percore
    y_pc = y_all // cores_num

    # x_remain, y_remain, num_remain
    y_rem = y_all % cores_num

    parse_image = [Image(x_pixels=x_all, y_pixels=y_pc, num_channels=num_all) for _ in range(cores_num)]

    # store image to parsed blank image
    for core in range(cores_num):
        for i in range(x_all):
            for j in range(y_pc):
                for k in range(num_all):
                    parse_image[core].array[i, j, k] = image.array[i , j + core * y_pc, k]

    with cf.ProcessPoolExecutor() as executor:
        filtered_images = list(executor.map(func, parse_image, [kernel] * cores_num))

    for core in range(cores_num):
        for i in range(x_all):
            for j in range(y_pc):
                for k in range(num_all):
                    new_image.array[i , j + core * y_pc, k] = filtered_images[core].array[i, j, k]

    return new_image


def guassian_blur(image, kernel_size):
    x_pixels, y_pixels, num_channels = image.array.shape
    neighbor_range = kernel_size // 2
    new_image = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)
    
    for x in tqdm(np.arange(x_pixels), desc="Processing", position=0, leave=True):
        for y in range(y_pixels):
            for c in range(num_channels):
                total = 0
                for x_i in range(max(0, x-neighbor_range), min(x_pixels-1, x+neighbor_range)+1):
                    for y_i in range(max(0, y-neighbor_range), min(y_pixels-1, y+neighbor_range)+1):
                        total += image.array[x_i, y_i , c]
                new_image.array[x, y, c] = total / (kernel_size **2)
    return new_image

def edge_detection(image, kernel):
    # the kernel should be a 2D array that represents the kernel we'll use!
    # for the sake of simiplicity of this implementation, let's assume that the kernel is SQUARE
    # for example the sobel x kernel (detecting horizontal edges) is as follows:
    # [1 0 -1]
    # [2 0 -2]
    # [1 0 -1]

    x_pixels, y_pixels, num_channels = image.array.shape
    new_image = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)  
    
    kernel_size = kernel.shape[0]
    neighbor_range = kernel_size // 2

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                total = 0
                for x_i in range(max(0, x-neighbor_range), min(x_pixels-1, x+neighbor_range)+1):
                    for y_i in range(max(0, y-neighbor_range), min(y_pixels-1, y+neighbor_range)+1):
                        x_k = x_i + neighbor_range - x
                        y_k = y_i + neighbor_range - y
                        kernel_val = kernel[x_k, y_k]
                        total += image.array[x_i, y_i, c] * kernel_val
                # black and white only to add colors include c below in brackets
                new_image.array[x, y]  = total
    return new_image
'''
def median_filter(image, kernel_size):
    x_pixels, y_pixels, num_channels = image.array.shape
    new_image = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    neighbor_range = kernel_size // 2

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                values = []
                for x_i in range(max(0, x-neighbor_range), min(x_pixels, x+neighbor_range+1)):
                    for y_i in range(max(0, y-neighbor_range), min(y_pixels, y+neighbor_range+1)):
                        values.append(image.array[x_i, y_i, c])

                values.sort()
                median_index = len(values) // 2
                new_image.array[x, y, c] = values[median_index]

    return new_image
'''





