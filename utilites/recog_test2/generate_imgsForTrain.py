import os
from pickle import FALSE, TRUE#?
from PIL import Image# mod image
import shutil#copy image file
import random
import uuid#unick names for images
import pandas as pd #pip install pandas
#import cv2
#pip install opencv-python
#opencv_python-4.13.0.92

widthGL, heightGL = 200, 200
datasetFolder = r".\dataset\images"
newImageMode = "RGB"
#фоны
def getBacksImgFromScreenshots():    
    x, y = 100, 350
    imgShop = Image.open(".\dataset\Isaac_3eTD5cCqeC.png")
    imgShopCropped = imgShop.crop((x, y, x+widthGL, y+heightGL))
    x, y = 100, 350
    imgDevil = Image.open(".\dataset\Isaac_5wuX8Aq31h.png")
    imgDevilCropped = imgDevil.crop((x, y, x+widthGL, y+heightGL))
    x, y = 650, 300
    imgBoss = Image.open(".\dataset\Isaac_jLexJZq15A.png")
    imgBossCropped = imgBoss.crop((x, y, x+widthGL, y+heightGL))
    x, y = 650, 200
    imgDoski = Image.open(".\dataset\Isaac_ltMKQBAIFR.png")
    imgDoskiCropped = imgDoski.crop((x, y, x+widthGL, y+heightGL))
    #imgDoskiCropped.show()
    #imgDevilCropped.show()
    #imgBossCropped.show()
    return [imgShopCropped, imgDevilCropped, imgBossCropped, imgDoskiCropped]

def getRockChestHeartImgs():  
    return [('rock', Image.open(r".\dataset\rock.png")),
    ('chest', Image.open(r".\dataset\chest.png")),
    ('heart1', Image.open(r".\dataset\heart1.png")),
    ('heart2', Image.open(r".\dataset\heart2.png"))]

def fixFolderName(name):
    return name.replace('?','_') # ???'s Soul

def CreateFoldersAndCopyImgs(img, imgName, isForTrain):        
    datasetFolder2 = ''
    if isForTrain:
        datasetFolder2 = 'train'
    else:
        datasetFolder2 = 'val'
    imgDirName = fixFolderName(imgName)
    #create folder
    destination = os.path.join(datasetFolder, datasetFolder2, imgDirName)
    if os.path.exists(destination) == False:
        os.makedirs(destination)
    #img name unick and save
    unique_id = uuid.uuid4().hex[0:4]
    #imgNameUnick = imgName.replace('.webp','_'+unique_id +'.webp')
    imgNameUnick = imgDirName +'_'+unique_id +'.webp'
    img.save(destination + '\\'+ imgNameUnick)

#from 70x70 to 200x200
def getExpandItemImgsWname(combined_df):
    for ind, row in combined_df.iterrows():#.itertuples():
        itemPath = row['imgSrc_dataset']        
        #imgName = row['imgName']
        itemCanvas= Image.new("RGBA", (widthGL, heightGL)) #RGBA
        itemImg = Image.open(itemPath)
        bw, bh = itemCanvas.size
        fw, fh = itemImg.size
        # координаты центра
        x = (bw - fw) // 2
        y = (bh - fh) // 2
        # вставляем картинки
        itemCanvas.paste(itemImg, (x, y), itemImg)
        #itemCanvas.show()
        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('image',img)
        #cv2.imwrite(".//saved_image.jpg", img)

        yield (ind, itemCanvas)#name for sorting and save folder
 
#фоны + предметы
def getJoinedItemAndBackImgsWname(combined_df, backImgs, rockChestHeartImgs):
    for ind, row in combined_df.iterrows():#.itertuples():
        isTrinket = row['isTrinket']
        #open image
        itemPath = row['imgSrc_dataset']
        itemImg = Image.open(itemPath)

        if not isTrinket:
            for backImg in backImgs:#random.shuffle(backImgs):
                bw, bh = backImg.size
                fw, fh = itemImg.size
                # координаты центра
                x = (bw - fw) // 2
                y = (bh - fh) // 2
                for rockType, rockImg in rockChestHeartImgs:
                    itemWithBack = Image.new(newImageMode, (widthGL, heightGL)) 
                    # вставляем фон
                    itemWithBack.paste(backImg, (0, 0))
                    # вставляем камень
                    if 'heart' in rockType:
                        itemWithBack.paste(rockImg, (x+10, y+30), rockImg)   
                    else:
                        itemWithBack.paste(rockImg, (x, y), rockImg)
                    # вставляем обхект
                    itemWithBack.paste(itemImg, (x, y-50), itemImg)# 3arg - mask
                    #itemWithBack.show()
                    yield (ind, itemWithBack) #itemId чтобы найти в списке а то они дублируются из за соединения фонов
        else:
            #add new backgroud
            backImgTinketShelf = shelfTrinket()
            backImgs2 = backImgs[:]
            backImgs2.insert(0,backImgTinketShelf)
            #do same
            for backImg in backImgs2:
                bw, bh = backImg.size
                fw, fh = itemImg.size
                # координаты центра
                x = (bw - fw) // 2
                y = (bh - fh) // 2
                itemWithBack = Image.new(newImageMode, (widthGL, heightGL))
                # вставляем фон
                itemWithBack.paste(backImg, (0, 0))
                # вставляем обхект
                itemWithBack.paste(itemImg, (x, y), itemImg)# 3arg - mask
                yield (ind, itemWithBack) #itemId чтобы найти в списке а то они дублируются из за соединения фонов
            
            #shelf back
            
def shelfTrinket():
    shelfBack = Image.open(r".\dataset\trinket_shelf.png")
    shelfBack=shelfBack.convert('RGB')            
    bw, bh = widthGL, heightGL
    fw, fh = shelfBack.size
    # координаты центра
    x = (bw - fw) // 2
    y = (bh - fh) // 2
    itemWithBack = Image.new(newImageMode, (widthGL, heightGL))
    # вставляем фон
    itemWithBack.paste(shelfBack, (x, y))
    '''
    # вставляем обхект
    bw, bh = widthGL, heightGL
    fw, fh = itemImg.size
    # координаты центра
    x = (bw - fw) // 2
    y = (bh - fh) // 2
    itemWithBack.paste(itemImg, (x, y), itemImg)# 3arg - mask
    '''
    #itemWithBack.show()
    return itemWithBack #itemId чтобы найти в списке а то они дублируются из за соединения фонов
            
#load dataset items
dataset_df = pd.read_csv(r'.\dataset\dataset.csv', encoding = 'utf-8')
'''
#test small df
dataset_df = (
    dataset_df[dataset_df['isTrinket'].isin([True, False])]
    .groupby('isTrinket', as_index =True)
    .apply(lambda x: x.sample(n=3))
)
dataset_df = dataset_df.reset_index()
'''
#filter trinket only
dataset_df = dataset_df[dataset_df['isTrinket'] == False]

# сгенерировать картинки
#   предметы с x70 на x200 без растягивания - для тренировки
print('expandItemImgs')
itemExpandedImgs = getExpandItemImgsWname(dataset_df)
#   предметы + фоны - для тренировки и обучения
print('joinItemAndBackImgs')
backImgs = getBacksImgFromScreenshots()
rockChestHeartImgs = getRockChestHeartImgs()
itemAndBackImgs = getJoinedItemAndBackImgsWname(dataset_df, backImgs, rockChestHeartImgs)

# скопировать картинки в yolo датасет 
# для обучения - альфа
# skip train cus have 4 channel. make 3?

print('copy expandItemImgs')
for itemdId, itemImgg  in itemExpandedImgs:
    row = dataset_df.loc[itemdId]
    #imgName = row['imgName']
    nameEN = row['nameEN']
    itemImgg = itemImgg.convert('RGB')
    CreateFoldersAndCopyImgs(itemImgg, nameEN, isForTrain=True)   

print('copy joinItemAndBackImgs')
# для обучения И для валидации - с фоном и камнем
backsCnt = len(backImgs)
rockChestHeartImgsCnt = len(rockChestHeartImgs)
print('backsCnt', backsCnt, 'rockChestHeartImgsCnt', rockChestHeartImgsCnt)#у брелков только фоны, у предметов фоны*камни
dividerTrinket = 3 #backsCnt / 2
dividerItem = 10 # 17  backsCnt * rockChestHeartImgsCnt / 2

imgNameCounter = 0
imgNamePrev = ''
isForTrain = True
#имена повторяются из-за перебора фонов, упорядочаны по названию чтоб по названию опеределять повторение
for i, (itemdId, itemImgg)  in enumerate(itemAndBackImgs):
    if i % 100 == 0:
        print(i,'/', len(dataset_df)*backsCnt * rockChestHeartImgsCnt )

    row = dataset_df.loc[itemdId]
    imgName = row['imgName']
    nameEN = row['nameEN']
    isTrinket = row['isTrinket']
    
    #таже картинка
    if(imgNamePrev == imgName or i==0):
        imgNameCounter+=1
    #смена картинки
    else:
        imgNameCounter=0
        isForTrain=False
    #картики повтарились n раз то копируем в валидацию а не в тренинг
    if(isTrinket and imgNameCounter >= dividerTrinket or isTrinket==False and imgNameCounter > dividerItem):
        isForTrain=False
    else:
        isForTrain = True
    imgNamePrev = imgName
    CreateFoldersAndCopyImgs(itemImgg, nameEN, isForTrain=isForTrain)   

#data.yaml
nameENs = dataset_df["nameEN"].to_list()
for i,p in enumerate(nameENs):
    print(i,":", fixFolderName(p))
    #0: class_001
    #1: class_002

with open('./dataset/data.yaml', 'w') as f:
    f.writelines(['path: dataset/images\n'])
    f.writelines(['train: train\n'])
    f.writelines(['val: val\n'])
    f.writelines(['names:\n'])
    f.writelines( [str(i)+":"+ fixFolderName(p)+'\n' for i,p in enumerate(nameENs)] )

print('ImageMode', newImageMode)
    


    
