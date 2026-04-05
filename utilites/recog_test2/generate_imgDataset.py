#save imgs dataset
from PIL import Image
import pandas as pd

width, height = 100, 100 #img size 1 for all
tableColumnCnt = 10

def getExpandItemImgsWname(df):
    for datasetInd, row in all_df.iterrows():#.itertuples():
        itemPath = row['imgSrc_dataset']        
        #imgName = row['imgName']
        itemCanvas= Image.new("RGBA", (width, height))
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
        yield (datasetInd, itemCanvas)#name for sorting and save folder

def generateImgDataset(df):
    itemExpandedImgsForDatasetImgs = list(getExpandItemImgsWname(df))
    tableRowCnt = int(len(itemExpandedImgsForDatasetImgs) / tableColumnCnt ) + 1# + 1 cus start from 1
    colNum = 0
    rowNum = 0
    itemCanvas= Image.new("RGBA", (width*tableColumnCnt, height*tableRowCnt))
    for i, (datasetInd, itemExpandedImgsForDatasetImg) in enumerate(itemExpandedImgsForDatasetImgs, 1): #start with 1 cus 0 - breaks line counter logic
        row = all_df.iloc[datasetInd]
        itemPath = row['imgSrc_dataset']
        itemImg = Image.open(itemPath)
        x = width * colNum #columns every item
        y = height * rowNum #rows every 10 items    
        if (i % tableColumnCnt  == 0): #and i !=0):#next row  . 0%0=0
            colNum = 0 #reset
            rowNum += 1#add
        else:#same row
            colNum +=1
        # вставляем картинки
        print('i', i, 'datasetInd', datasetInd,'col',colNum,'row',rowNum, row['nameEN'] )
        itemCanvas.paste(itemImg, (x, y+height), itemImg)
    itemCanvas.save('dataset.webp')

def getImgFromDataset(ind):
    colNum = ind % tableColumnCnt
    rowNum = int(ind / tableColumnCnt)
    x = width * colNum #columns every item
    y = height * rowNum #rows every 10 items
    #print(colNum, rowNum)
    datasetImg = Image.open('./dataset.webp')
    box = (x, y, x+width, y+height) # (left, upper, right, lower)
    cropped_img = datasetImg.crop(box)
    return cropped_img

all_df = pd.read_csv(r'.\dataset\dataset.csv', encoding = 'utf-8')
generateImgDataset(all_df)
#img = getImgFromDataset(5)
#img.show()

