import importlib.metadata
__version__ = importlib.metadata.version('seg')

import os.path
import math
import matplotlib.pyplot as plt
import cv2

DATA_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/data'

def load_dataset(id = 'seh', display = True):
    '''
    load bult-in dataset by id
    '''
    if id == 'seh' or id == 'SEH':
        folder = DATA_FOLDER + '/SEH'
        imgs = []
        for img_path in os.listdir(folder):
            if img_path.endswith('.jpg'):
                img = cv2.imread(folder + '/' + img_path)
                img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                imgs.append(img)

        if display:
            fig, ax = plt.subplots(nrows= math.ceil(len(imgs)/5.0), ncols=5, figsize=(13, math.ceil(len(imgs)/5.0)*2))
            ax = ax.flatten()
            
            for idx, axi in enumerate(ax):
                if idx < len(imgs):
                    axi.imshow(imgs[idx])
                axi.axis('off')
            plt.tight_layout()
            plt.show()

        return imgs
    else:
        raise RuntimeError('Please check dataset id. Accepted values are: SEH.')