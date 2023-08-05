import pandas as pd
import os
from pathlib import Path
import zipfile
import requests
from glob import glob
from apng import APNG


dir_path = Path(os.path.dirname(os.path.realpath(__file__)))

def get_animation(productId, location='./_tmp'):
    productId = str(productId)
    location = Path(location)
    location.mkdir(exist_ok=True)
    dataLocation = location / "data"
    dataLocation.mkdir(exist_ok=True)
    zipFilePath = location / f'{productId}.zip'
    if not zipFilePath.exists():
        zipFile = requests.get(f'http://dl.stickershop.line.naver.jp/products/0/0/1/{productId}/iphone/stickerpack@2x.zip', timeout=10)
        with open(zipFilePath, 'wb') as f:
            f.write(zipFile.content)
    extractLocation = location / productId
    if not extractLocation.exists():
        with zipfile.ZipFile(zipFilePath, 'r') as zip_ref:
            zip_ref.extractall(extractLocation)
    extractLocation /= "animation@2x"

    
    dataset = []
    for file in glob(str(extractLocation / "*.png")):
        im = APNG.open(file)
        animations = []
        for i, (png, control) in enumerate(im.frames):
            path = dataLocation / f"{Path(file).name.split('.')[0]}_{i}.png"
            png.save(path)
            animations.append(str(path))
        dataset.append(animations)
    return dataset

def get_animation_data(num_set, location='./_tmp'):
    """ total 7107 """
    df = pd.read_csv( dir_path / f'linesticker_animation.csv')
    print("total # set", len(df))
    dataset = []
    for i, row in df.iterrows():
        if i >= num_set:
            break
        data = get_animation(row['productId'])
        dataset.extend(data)
    return dataset