import os
#pip install ultralytics
print('import yolo')
from ultralytics import YOLO

#--train
#Download weights from https://learnopencv.com/ultralytics-yolov8/
# -cls for classification
#start train not in IDE
mod = "yolov8m-cls.pt" #med
#mod = "yolov8n-cls.pt" #nano
model = YOLO(mod)  # load a pretrained model
model.train(
    data=".\dataset\images",#data.yaml
    epochs=50,
    imgsz=200,
    batch=12
)
#--test model on my images
# после обучения Файл модели появится в: runs/detect/train/weights/best.pt
print('start yolo')
modelPath = r".\runs\classify\1_train50epochRGBandAlpha8m\weights\best.pt"
modelPath = r".\runs\classify\train\weights\best.pt"
model = YOLO(modelPath )

imgDirItem=r".\dataset\testImgs"
imgsItemsPaths = [os.path.join(imgDirItem, i) for i in os.listdir(imgDirItem) if len(i.split('.'))>1]
print('///', modelPath)

for imgsItemsPath in imgsItemsPaths:
    print('--',os.path.basename(imgsItemsPath))
    results = model(imgsItemsPath)

    classes1 = results[0].probs.top1
    scores = results[0].probs.top1conf
    print(results[0].names[classes1])
    print(scores )
    #results[0].show()
