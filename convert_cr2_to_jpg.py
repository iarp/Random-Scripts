# pip install Image
# pip install rawpy
# pip install imageio

import glob
import rawpy
import os
import imageio


target = r'C:\cr2-images\*.cr2'
cache = 'cache/'

os.makedirs(cache, exist_ok=True)


for file in glob.glob(target, recursive=True):
    print(file)
    filename, ext = os.path.basename(file).rsplit('.', 1)
    cache_file_path = f'{cache}/{filename}.jpg'

    if os.path.isfile(cache_file_path):
        continue

    with rawpy.imread(file) as raw:
        rgb = raw.postprocess()

    imageio.imsave(cache_file_path, rgb)
