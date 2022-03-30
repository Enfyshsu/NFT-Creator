#!/usr/bin/env python
# coding: utf-8

# https://betterprogramming.pub/create-your-own-nft-collection-with-python-82af40abf99f
from django.conf import settings
from PIL import Image 
from IPython.display import display 
import zipfile
import random
import json
import os
import shutil

def main(zip_filename, image_num, uuid):
    all_types = [t.split('.')[0] for t in os.listdir(zip_filename) if not t.startswith('.')]
    all_types.sort()

    all_files = {}

    for t in all_types:
        all_files[t] = [f.split('.')[0] for f in os.listdir(os.path.join(zip_filename, t)) if not f.startswith('.')]

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
    for i in range(image_num): 
        new_trait_image = create_new_image()
        new_trait_image["id"] = i
        all_images.append(new_trait_image)

    #### Generate Images
    os.mkdir(settings.MEDIA_ROOT + '/' + uuid)
    path = settings.MEDIA_ROOT + '/' + uuid + '/images/'
    os.mkdir(path)

    for img in all_images:
        img_list = {}
        for i in range(len(all_types)):
            img_list["img_" + str(i)] = Image.open(os.path.join(zip_filename, all_types[i], img[all_types[i]] + '.png')).convert('RGBA')
        
        composite_img = Image.alpha_composite(img_list["img_0"], img_list["img_1"])
        for i in range(2, len(all_types)):
            composite_img = Image.alpha_composite(composite_img, img_list["img_" + str(i)])

        rgb_im = composite_img.convert('RGB')
        file_name = str(img["id"]) + ".png"
        rgb_im.save(path + file_name)

    # write data.csv
    import csv  

    header = all_types.copy()
    header.insert(0, 'Name')

    with open(settings.MEDIA_ROOT + '/' + uuid + '/data.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for img in all_images:
            data = []
            data.append(img["id"])
            for t in all_types:
                data.append(img[t])
            writer.writerow(data)

    shutil.rmtree(zip_filename)

    startdir = settings.MEDIA_ROOT + '/' + uuid
    file_news = startdir + '.zip'
    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(startdir):
        fpath = dirpath.replace(startdir, '')
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames:
            z.write(os.path.join(dirpath, filename), fpath + filename)
    z.close()

if __name__ == "__main__":
    main(zip_filename, image_num, uuid)