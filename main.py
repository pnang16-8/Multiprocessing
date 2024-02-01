import concurrent.futures as cf
import time
from transform_M import *
import numpy as np
from image import Image

def main():
    
    '''
    st = time.perf_counter()
    
    blur_lake = blur(lake,3)
    blur_lake.write_image("blur_lake.png")
    et = time.perf_counter()
    print(f"Used time Thread:{et-st}.")
    
    
    st = time.perf_counter()
    with cf.ProcessPoolExecutor() as executor:
        blur_lake2 = executor.submit(blur, lake, 3)
        result = blur_lake2.result()
        result.write_image("blur_lake2.png")
    et = time.perf_counter()
    print(f"Used time Multi:{et-st}.")
    
    n = 50
    lake = [Image(filename="lake.png")]*n
    kernel = [3]*n
    
    st = time.perf_counter()
    
    with cf.ProcessPoolExecutor() as executor:
        blur_lake = list(executor.map(guassian_blur,lake, kernel))
        for i, blurred_image in enumerate(blur_lake):
            executor.submit(blur_lake[i].write_image(f"blur_lakeMulti{i+1}.png"))
    
    et = time.perf_counter()

    print(f"Used time Thread:{et-st}.")

    #blur normal
    st = time.perf_counter()
    blur_lake = list(map(blur, lake, kernel))
    #blur_lake = blur(lake,3)
    for i in range(len(blur_lake)):
        blur_lake[i].write_image(f"blur_lakeN{i+1}.png")

    et = time.perf_counter()
    print(f"Used time Thread:{et-st}.")
    '''
    #lake = Image(filename="lake.png")
    #new = parse_image(lake, guassian_blur,1)
    #new.write_image("test.png")
    #for i in range(len(new)):
        #new[i].write_image(f"test{i+1}.png")
    '''city = Image(filename="city.png")
    sobelX_kernel = np.array([[1, 0, -1],
                             [2, 0, -2],
                             [1, 0, -1]])
    sobelY_kernel = np.array([[1, 2, 1],
                             [0, 0, 0],
                             [-1, -2, -1]])
    edgeX_city = edge_detection(city, sobelX_kernel)
    edgeY_city = edge_detection(city, sobelY_kernel)
    edge_city = combine_images(edgeX_city,  edgeY_city)
    edge_city.write_image("Edge_city.png")'''
    
    '''city = Image(filename= 'city.png')

   
    kernel_size = 3

    
    median_filtered_city = median_filter(city, kernel_size)

   
    sobelX_kernel = np.array([[1, 0, -1],
                              [2, 0, -2],
                              [1, 0, -1]])

    sobelY_kernel = np.array([[1, 2, 1],
                              [0, 0, 0],
                              [-1, -2, -1]])

    
    median_filteredx_city = median_filter(median_filtered_city, sobelX_kernel)
    median_filteredy_city = median_filter(median_filtered_city, sobelY_kernel)


    combined_image = combine_images(median_filteredx_city, median_filteredy_city)

    
    combined_image.save("city_median.png")มันเจอErrorอะในmain''' 

if __name__ == "__main__": 
    main()