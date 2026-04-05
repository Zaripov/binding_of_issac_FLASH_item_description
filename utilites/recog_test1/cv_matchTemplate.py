import os
import cv2
#pip install opencv-python
#opencv_python-4.13.0.92
import numpy as np

# поиск картинок
imgDir1="imgForTest"
imgDir2="imgTemplate"
imgsForRecog = [(i, '.\\'+os.path.join(imgDir1,i)) for i in os.listdir('./'+imgDir1) if len(i.split('.'))>1]#skip folder
imgsTemplates = [(i, '.\\'+os.path.join(imgDir2,i)) for i in os.listdir('./'+imgDir2)]
imgsForRecogDict = {}#imgData = None
for imgName, path in imgsForRecog:
    #imgData.name = imgName
    #imgData.img = cv2.imread(path)
    imgsForRecogDict[imgName] = cv2.imread(path)#, cv2.IMREAD_GRAYSCALE)
imgsTemplateDict = {}
for imgName, path in imgsTemplates:    
    imgsTemplateDict[imgName] = cv2.imread(path)#, cv2.IMREAD_GRAYSCALE)

# All the 6 methods for comparison in a list https://docs.opencv.org/4.x/d4/dc6/tutorial_py_template_matching.html
methods1 = ('TM_CCOEFF', 'TM_CCOEFF_NORMED', 'TM_CCORR',
            'TM_CCORR_NORMED', 'TM_SQDIFF', 'TM_SQDIFF_NORMED')
#compare first method
def compareByMatchTemplate(imgForRecog, imgsTemplateDict):
    for imgTempalteName, imgTemplate in imgsTemplateDict.items():
        #Шаблон2 должен быть меньше или равен изображению1
        #result = cv2.matchTemplate(imgForRecog, imgTemplate, cv2.TM_CCOEFF_NORMED)
        for meth in methods1:
            print(' ', imgTempalteName, imgsTemplateDict[imgTempalteName].shape, meth, end=' ')
            method = getattr(cv2, meth)
 
            # Apply template Matching
            result = cv2.matchTemplate(imgForRecog,imgTemplate,method)
        
            _, max_val, _, _ = cv2.minMaxLoc(result)
            print(max_val)

#compare 2 method
def compareByOrb(imgForRecog, imgsTemplateDict):
        for imgTempalteName, imgTemplate in imgsTemplateDict.items():
             orb = cv2.ORB_create()
             #method = getattr(cv2, meth)
             #orb = method()
             
             kp1, des1 = orb.detectAndCompute(imgForRecog, None)
             kp2, des2 = orb.detectAndCompute(imgTemplate, None)
             bf = cv2.BFMatcher(cv2.NORM_HAMMING)
             print(' ', imgTempalteName, imgsTemplateDict[imgTempalteName].shape,'orb', end=' ')
             if des1 is None or des2 is None:
                print("No descriptors found")
             else:
                 matches = bf.match(des1, des2)
                 print(len(matches))

                 #result = cv2.drawMatches(imgsTemplateDict[imgTempalteName], kp1, imgForRecog, kp2, matches[:20], None)
                 #cv2.imshow("Matches", result)
                 #cv2.waitKey(0)
                 
def compareBySIFT(imgForRecog, imgsTemplateDict):
    for imgTempalteName, imgTemplate in imgsTemplateDict.items():
             orb = cv2.SIFT_create()

             kp1, des1 = orb.detectAndCompute(imgForRecog, None)
             kp2, des2 = orb.detectAndCompute(imgTemplate, None)
             bf = cv2.BFMatcher(cv2.NORM_L2)
             print(' ', imgTempalteName, imgsTemplateDict[imgTempalteName].shape,'SIFT', end=' ')
             matches = bf.match(des1, des2)
             print(len(matches))

             result = cv2.drawMatches(imgsTemplateDict[imgTempalteName], kp1, imgForRecog, kp2, matches[:20], None)
             cv2.imshow("Matches", result)
             cv2.waitKey(0)

def gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def blur(img):
     # Apply Gaussian Blur to reduce noise
    return cv2.GaussianBlur(img, (5, 5), 1.4)

def canny(img):
    #img = cv2.imread("image.png", cv2.IMREAD_UNCHANGED)  # сохраняет альфа канал
    # если есть альфа канал
    #if img.shape[2] == 4:
    #    img[:, :, 3] = 255   # заполнить альфа канал белым
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply Canny Edge Detector
    edges = cv2.Canny(img, threshold1=100, threshold2=200)
    return edges

imgsForRecogDict = {key: gray(value) for key, value in imgsForRecogDict.items()}
imgsForRecogDict = {key: blur(value) for key, value in imgsForRecogDict.items()}
imgsForRecogDict = {key: canny(value) for key, value in imgsForRecogDict.items()}

imgsTemplateDict = {key: gray(value) for key, value in imgsTemplateDict.items()}
imgsTemplateDict = {key: canny(value) for key, value in imgsTemplateDict.items()}

#print('cv2.matchTemplate Шаблон2 должен быть меньше или равен изображению1')
for imgForRecogName, imgForRecog in imgsForRecogDict.items():
    print(imgForRecogName, imgsForRecogDict[imgForRecogName].shape)
    #compareByMatchTemplate(imgForRecog, imgsTemplateDict)
    #compareByOrb(imgForRecog, imgsTemplateDict)
    compareBySIFT(imgForRecog, imgsTemplateDict)
    #cv2.imshow("Matches", imgForRecog)
    #cv2.waitKey(0)
    
