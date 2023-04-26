import os
import cv2
from glob import glob
import shutil



DATA_DIR = './mask-data'
SAVE_DIR = './split_mask-data'
DATA_SIZE = [80, 15, 5]

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def split_data(image, save_path):
    counter = 0
    
    for x in image:
        name_x = x.split("\\")[-1]
        y = x.replace('images', 'labels').replace('.png', '.txt')
        if counter <= DATA_SIZE[0]:
            file_path = os.path.join(save_path, 'train', "images")
        elif counter > DATA_SIZE[0] and counter <= DATA_SIZE[0] + DATA_SIZE[1]:
            file_path = os.path.join(save_path, 'val', "images")
        else:
            file_path = os.path.join(save_path, 'test', "images")
        
        image_path = os.path.join(file_path, name_x)
        label_path = os.path.join(file_path.replace('images', 'labels'), name_x.replace('.png', '.txt'))
        shutil.copy(x, image_path)
        shutil.copy(y, label_path)
        
        counter += 1

        if counter >= 100:
            counter = 0

if __name__ == '__main__':
    X = sorted(glob(os.path.join(DATA_DIR, "images", "*.png")))
    create_dir(os.path.join(SAVE_DIR, 'train', 'images',))
    create_dir(os.path.join(SAVE_DIR, 'train', 'labels',))
    create_dir(os.path.join(SAVE_DIR, 'val', 'images',))
    create_dir(os.path.join(SAVE_DIR, 'val', 'labels',))
    create_dir(os.path.join(SAVE_DIR, 'test', 'images',))
    create_dir(os.path.join(SAVE_DIR, 'test', 'labels',))
    split_data(X, SAVE_DIR)
    print('Finish')

