"""
Author: Zaripov gltlail999@gmail.com
Created: 2026-04-02
Description: item descriptiontool for game The Binding of Isaac (Flash) via yolo ai with tkinter interface
Link: https://github.com
"""
print('loading YOLO lib')
from ultralytics import YOLO#recognise

import mss #screenshot
import numpy as np #screenshot to img
import keyboard #hotkey. keyboard требует админских прав на Window
import pandas as pd #dataset read
import tkinter as tk #IDE
from PIL import Image, ImageTk #show image
import pyautogui  # mouse x y
import configparser #INI
import sys #show error

# --- SCREENSHOT ---
def capture_region(x, y, size=120):
    with mss.mss() as sct:
        monitor = {
            "top": y - size//2,
            "left": x - size//2,
            "width": size,
            "height": size
        }
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        return img

# --- OVERLAY popup window ---
class Overlay:
    def __init__(self, root, text, itemImg, itemUrl):
        self.win = tk.Toplevel(root)
        self.win.overrideredirect(True)  # withou frame
        self.win.attributes("-topmost", True)
        self.win.attributes("-alpha", alphaGL) #0.9

        # mouse pos
        x, y = pyautogui.position()
        self.win.geometry(f"+{x+20}+{y+20}")
        #screen_x = self.winfo_pointerx()
        #screen_y = self.winfo_poinery()
        #self.win.geometry(f"+{x+20}+{y+20}")
        
        # bg
        frame = tk.Frame(self.win, bg=frameBackGL) #black
        frame.pack()

        # show image
        try:
            #img = Image.open("chest.png")
            imgTk = ImageTk.PhotoImage(itemImg)
            panel = tk.Label(frame, image=imgTk, bg="black")
            panel.image = imgTk
            panel.pack()
        except:
            print("no img err")

        # descrtion
        font=(fontNameGL, fontSizeGL )#"TkDefaultFont" 12
        label = tk.Label(
            frame,
            text=text,
            fg=fontColorGL, #white  Font color
            bg=fontBackGL, #black Font backgroud
            justify="left",
            padx=10,
            pady=10,
            wraplength=wraplengthGL,# long text linebreak 250
            font=font
        )
        label.pack()
        # auto close after 5 sec
        self.win.after(selfDestroyTimeGL, self.win.destroy)
        '''
        #url label
        if(itemUrl!= ''):
            labelUrl = tk.Label(
                frame,
                text="ссылка",
                fg="blue", #white  Font color
                bg=fontBackGL, #black Font backgroud
                justify="left",
                padx=10,
                pady=10,
                wraplength=wraplengthGL,# long text linebreak 250
            )
            labelUrl.pack()
            labelUrl.bind("<Button-1>", lambda: open_url(itemUrl))
        '''
def open_url(event, itemUrl):
    import webbrowser
    webbrowser.open_new(itemUrl)

# --- YOLO recog ---
def recog_item(screenshot):
    results1 = modelItemGL(screenshot)
    results2 = modelTrinketGL(screenshot)

    scores1 = results1[0].probs.top1conf #уверенность
    scores2 = results2[0].probs.top1conf
    
    classesN1 = results1[0].probs.top1 #yolo ind
    classesN2 = results2[0].probs.top1 #yolo ind != dataset ind
    
    if scores1 > scores2:
        return scores1, results1[0].names[classesN1]#return yolo class name by yolo ind
    else:
        return scores2, results2[0].names[classesN2]


# --- get img from img dataset ---
def getImgFromDataset(ind):
    colNum = ind % tableColumnCntGL
    rowNum = int(ind / tableColumnCntGL) +1
    x = widthGL * colNum #columns every item
    y = heightGL * rowNum #rows every 10 items
    #print('colNum', colNum, 'rowNum', rowNum)
    #datasetImg = Image.open('./dataset.webp')
    box = (x, y, x+widthGL, y+heightGL) # (left, upper, right, lower)
    cropped_img = datasetImgGL.crop(box)
    return cropped_img

# --- HOTKEY ---
def on_hotkey():
    x, y = pyautogui.position()
    screenshot = capture_region(x, y)

    score, itemNameEn = recog_item(screenshot)
    itemNameEn = manualErrorFix(itemNameEn) #'Little C.H.A.D' from yolo 'Little C.H.A.D.'
    #get data from dataset csv
    rows_with_item = dataset_dfGL.loc[dataset_dfGL['nameEN'] == itemNameEn] # find by item name. model trained by item nameEN
    if not rows_with_item.empty:
        #get text
        nameRu = rows_with_item[langColsDictGL[langGL][0]].values[0]#'nameRU'
        descr = rows_with_item[langColsDictGL[langGL][1]].values[0]#'descrRU'
        reload = rows_with_item['reloadCnt'].values[0]
        isPassive = rows_with_item['isPassive'].values[0]
        link = ''
        if langGL=='ru':
            link = rows_with_item['urlToPageRU'].values[0]
        
        text = f"{nameRu}\n{descr}\nreload:{reload}\nisPassive:{isPassive}\nscore:{score}"
        print(text)
        #get img from dataset
        itemIndDataset = rows_with_item.index.values[0]
        itemImg = getImgFromDataset(itemIndDataset)
        #print('Ind dataset', itemIndDataset, 'Ind Yolo', itemIndYolo)
        #show window
        global overlay #save window (after func end) for destroy by time
        overlay = Overlay(root, text, itemImg, link)
    else:
        print('not find in dataset csv')

def manualErrorFix(nameFromYolo):
    if nameFromYolo == 'Little C.H.A.D':
        return 'Little C.H.A.D.'
    return nameFromYolo

# --- MAIN ---
def main():
    global root
    root = tk.Tk()
    root.withdraw()  # скрыть основное окно
    root.mainloop()

if __name__ == '__main__':
    with open('error_log.txt', 'a') as f: #save errors
        sys.stderr = f
        try:
            #load settings from ini file
            config = configparser.ConfigParser(inline_comment_prefixes=(';', '#'))
            config.read('settings.ini')
            selfDestroyTimeGL = config.get('interface','selfDestroyTime') #5000 #auto destroy window after 5sec
            user_hotkey = config.get('interface', 'hotkey') 
            keyboard.add_hotkey(user_hotkey, on_hotkey)#set hotkey
            langGL = config.get('interface','lang')
            langColsDictGL = {'ru': ('nameRU','descrRU'), 'en':('nameEN','descrEN_trans')}#gets different column from dataset csv depending on the language
            fontSizeGL = config.get('interface','fontSize')
            fontNameGL = config.get('interface','fontName')
            alphaGL = config.get('interface','alpha')
            wraplengthGL = config.get('interface','wraplength')
            fontColorGL = config.get('interface','fontColor')
            fontBackGL = config.get('interface','fontBack')
            frameBackGL = config.get('interface','frameBack')
            #staic settings
            imgDatasetPath = r".\dataset.webp"
            darasetPath = r".\dataset.csv"
            #load datasets
            dataset_dfGL = pd.read_csv(darasetPath, encoding = 'utf-8')
            datasetImgGL = Image.open('./dataset.webp')
            tableColumnCntGL = 10 #img dataset column count
            widthGL, heightGL = 100, 100 #item img size 1 for all in dataset img
            #load models
            #modelPath = r"E:\_projects copy 24.03.18\_archive\python AI\binding of issac FLASH item description\utilites\recog_test2\runs\classify"
            #modelPath1 = modelPath + r"\train\weights\best.pt"
            #modelPath2 = modelPath + r"\train5\weights\best.pt"
            modelPath1 = r".\ItemModel.pt"
            modelPath2 = r".\TrinketModel.pt"
            modelItemGL = YOLO(modelPath1)
            modelTrinketGL = YOLO(modelPath2)

            if langGL == 'ru':
                print("Наведи курсор на предмет и нажми " + user_hotkey)
            else:
                print("Hover over the item and push " + user_hotkey)
            #start interface
            main()
        except Exception:
            import traceback
            traceback.print_exc()
