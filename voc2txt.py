import os, shutil
from bs4 import BeautifulSoup

rootFolder = 'mask-data'
annotations = os.path.join(rootFolder, 'annotations')
destination = os.path.join(rootFolder, 'labels')

if not os.path.exists(destination):
    os.mkdir(destination)

className = ['with_mask', 'without_mask', 'mask_weared_incorrect']

for xmlFile in os.listdir(annotations):
    with open(os.path.join(annotations, xmlFile), 'r', encoding="UTF-8") as voc:
        bsObj = BeautifulSoup(voc.read(), 'lxml')
        picFilename = bsObj.select_one('filename').get_text()
        picW = bsObj.select_one('size width').get_text()
        picH = bsObj.select_one('size height').get_text()
        
        objectAttrs = []
        for bndBox in bsObj.select('object'):
            name = bndBox.select_one('name').get_text()
            xmin = bndBox.select_one('xmin').get_text()
            xmax = bndBox.select_one('xmax').get_text()
            ymin = bndBox.select_one('ymin').get_text()
            ymax = bndBox.select_one('ymax').get_text()
            
            classId = className.index(name)
            xcenter = eval(f'({xmin}+{xmax})/2/{picW}')
            ycenter = eval(f'({ymin}+{ymax})/2/{picH}')
            bndBoxW = eval(f'({xmax}-{xmin})/{picW}')
            bndBoxH = eval(f'({ymax}-{ymin})/{picH}')
            
            objectAttrs.append(f'{classId} {xcenter} {ycenter} {bndBoxW} {bndBoxH}')
        with open(os.path.join(destination, os.path.splitext(picFilename)[0]) + '.txt', 'w', encoding='UTF-8') as yoloTxt:
            yoloTxt.write('\n'.join(objectAttrs))