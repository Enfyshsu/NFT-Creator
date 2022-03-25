#!/usr/bin/env python
# coding: utf-8

# https://betterprogramming.pub/create-your-own-nft-collection-with-python-82af40abf99f

from PIL import Image 
from IPython.display import display 
import random
import json
import os
import shutil

def main(zip_filename, total_images):

    all_types = os.listdir(zip_filename)
    all_types.sort()

    all_files = {}

    for t in all_types:
        all_files[t] = []
        for f in os.listdir(os.path.join(zip_filename, t)):
           all_files[t].append(f)

    ## Generate Traits

    all_images = [] 
    # A recursive function to generate unique image combinations
    def create_new_image():
        
        new_image = {} #

        # For each trait category, select a random trait based on the weightings 
        for t in all_types:
            new_image[t] = random.choice(all_files[t])
        
        return new_image if new_image not in all_images else create_new_image()

        
        
    # Generate the unique combinations based on trait weightings
    for i in range(total_images): 
        new_trait_image = create_new_image()
        new_trait_image["id"] = i
        all_images.append(new_trait_image)
    
    # print(all_images)

    #### Generate Images

    path= f'./images'
    if os.path.exists(path):
        # 遞迴刪除資料夾下的所有子資料夾和子檔案
        shutil.rmtree(path)
    os.mkdir(path)

    for img in all_images:
        img_list = {}
        for i in range(len(all_types)):
            img_list["img_" + str(i)] = Image.open(os.path.join(zip_filename, all_types[i], img[all_types[i]])).convert('RGBA')
        
        composite_img = Image.alpha_composite(img_list["img_0"], img_list["img_1"])
        for i in range(2, len(all_types)):
            composite_img = Image.alpha_composite(composite_img, img_list["img_" + str(i)])

        rgb_im = composite_img.convert('RGB')
        file_name = str(img["id"]) + ".png"
        rgb_im.save("./images/" + file_name)

    # write data.csv
    import csv  

    header = all_types

    with open('data.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for img in all_images:
            data = []
            for t in all_types:
                data.append(img[t])
            writer.writerow(data)


    shutil.rmtree(zip_filename)
if __name__ == "__main__":
    main(zip_filename, total_images)