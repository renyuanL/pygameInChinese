'''
滑動拼圖

中文翻譯： 曹祐，呂仁園。

'''

# Slide Puzzle
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import pygame, sys, random
from pygame.locals import *

from pygame_tc import *

# 加上這行，可以用中文命名 py game 函數
# 目前可用函數如下，可以進一步擴充。

'''
範圍=  range


啟動=     pygame.init
鐘類=     pygame.time.Clock
幕設大小= pygame.display.set_mode
幕設標題= pygame.display.set_caption
字型類=   pygame.font.Font
影像下載= pygame.image.load

轉換平滑尺度= pygame.transform.smoothscale

聲音類=   pygame.mixer.Sound

事件取得= pygame.event.get
結束=     pygame.quit
離開=     sys.exit
隨機選擇= random.choice
畫方形=   pygame.draw.rect
深層複製= copy.deepcopy


事件取得= pygame.event.get
幕更新=   pygame.display.update

系統離開= sys.exit

事件張貼= pygame.event.post

方塊類=   pygame.Rect

時間等待= pygame.time.wait
'''

行數 = 4
列數 = 4
方塊尺寸 = 80
視窗寬度 = 640
視窗高度 = 480
畫面更新率 = 30
空白 = None

#         R    G    B
黑色 = (  0,   0,   0)
白色 = (255, 255, 255)
亮藍 = (  0,  50, 255)
墨綠 = (  3,  54,  73)
綠色 = (  0, 204,   0)
背景顏色 = 墨綠
方塊顏色 = 綠色
文字顏色 = 白色
邊框顏色 = 亮藍

基本字體大小 = 20
按鈕顏色 = 白色
按鈕文字顏色 = 黑色
訊息顏色 = 白色
邊框X座標 = int((視窗寬度 - (方塊尺寸 * 行數 + (行數 - 1))) / 2)
邊框Y座標 = int((視窗高度 - (方塊尺寸 * 列數 + (列數 - 1))) / 2)

上 = '上'
下 = '下'
左 = '左'
右 = '右'

def main():

    global 畫面更新控制器, 顯示介面, 基本字型, 重置介面, 重置方塊, 新介面, 新方塊, 解答畫面, 解答方塊

    pygame.init()

    畫面更新控制器 = pygame.time.Clock()
    顯示介面 = pygame.display.set_mode((視窗寬度, 視窗高度))

    pygame.display.set_caption('Slide Puzzle, 滑動拼圖')
    基本字型 = pygame.font.Font('freesansbold.ttf', 基本字體大小)


    重置介面, 重置方塊 = 製造文字('ReSet',文字顏色,方塊顏色,視窗寬度 - 120,視窗高度 - 90)
    新介面, 新方塊   = 製造文字('New Game', 文字顏色, 方塊顏色, 視窗寬度 - 120, 視窗高度 - 60)

    解答畫面, 解答方塊 = 製造文字('Solve',文字顏色, 方塊顏色, 視窗寬度 - 120, 視窗高度 - 30)

    主要區塊, 解答順序 = 產生新題目(80)
    解答區塊 = 區塊初始化()
    移動記錄 = []

    while True:
        滑向 = None
        訊息 = ''
        if 主要區塊 == 解答區塊:
             訊息 = 'Solved! 已解！'

        繪製畫面(主要區塊, 訊息)

        結束檢查()
        for event in pygame.event.get():
             if event.type == MOUSEBUTTONUP:
                點擊橫座標, 點擊縱座標 = 取得點擊座標(主要區塊, event.pos[0], event.pos[1])

                if (點擊橫座標, 點擊縱座標) == (None, None):
                    # check if the user clicked on an option button
                     if 重置方塊.collidepoint(event.pos):
                         重置動畫(主要區塊, 移動記錄) # clicked on Reset button
                         移動記錄 = []
                     elif 新方塊.collidepoint(event.pos):
                         主要區塊, 解答順序 = 產生新題目(80) # clicked on New Game button
                         移動記錄 = []
                     elif 解答方塊.collidepoint(event.pos):
                         重置動畫(主要區塊, 解答順序 + 移動記錄) # clicked on Solve button
                         移動記錄 = []
                else:

                     空位橫座標, 空位縱座標 = 取得空位置(主要區塊)
                     if 點擊橫座標 == 空位橫座標 + 1 and 點擊縱座標 == 空位縱座標:
                         滑向 = 左
                     elif 點擊橫座標 == 空位橫座標 - 1 and 點擊縱座標 == 空位縱座標:
                         滑向 = 右
                     elif 點擊橫座標 == 空位橫座標 and 點擊縱座標 == 空位縱座標 + 1:
                         滑向 = 上
                     elif 點擊橫座標 == 空位橫座標 and 點擊縱座標 == 空位縱座標 - 1:
                         滑向 = 下

             elif event.type == KEYUP:
                # check if the user pressed a key to slide a tile
                if event.key in (K_LEFT, K_a) and 有效移動(主要區塊, 左):
                    滑向 = 左
                elif event.key in (K_RIGHT, K_d) and 有效移動(主要區塊, 右):
                    滑向 = 右
                elif event.key in (K_UP, K_w) and 有效移動(主要區塊, 上):
                    滑向 = 上
                elif event.key in (K_DOWN, K_s) and 有效移動(主要區塊, 下):
                    滑向 = 下

        if 滑向:
            移動動畫(主要區塊, 滑向, 'Click tile or press arrow keys to slide. 點擊小方塊或按方向鍵來滑動。', 8) # show slide on screen
            移動函式(主要區塊, 滑向)
            移動記錄.append(滑向) # record the slide
        pygame.display.update()
        畫面更新控制器.tick(畫面更新率)


def 終止():
    pygame.quit()
    sys.exit()


def 結束檢查():
    for event in pygame.event.get(QUIT):
        終止()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            終止()
        pygame.event.post(event)


def 區塊初始化():
    計數器 = 1
    方塊 = []
    for 橫座標 in range(行數):
         行 = []
         for 縱座標 in range(列數):
             行.append(計數器)
             計數器 += 行數
         方塊.append(行)
         計數器 -= 行數 * (列數 - 1) + 行數 - 1

    方塊[行數-1][列數-1] = None
    return 方塊


def 取得空位置(方塊):
    for 橫座標 in range(行數):
        for 縱座標 in range(列數):
            if 方塊[橫座標][縱座標] == None:
                return (橫座標, 縱座標)

def 移動函式(方塊, 移動):
    空位橫座標, 空位縱座標 = 取得空位置(方塊)

    if 移動 == 上:
        方塊[空位橫座標][空位縱座標], 方塊[空位橫座標][空位縱座標 + 1] = 方塊[空位橫座標][空位縱座標 + 1], 方塊[空位橫座標][空位縱座標]
    elif 移動 == 下:
        方塊[空位橫座標][空位縱座標], 方塊[空位橫座標][空位縱座標 - 1] = 方塊[空位橫座標][空位縱座標 - 1], 方塊[空位橫座標][空位縱座標]
    elif 移動 == 左:
        方塊[空位橫座標][空位縱座標], 方塊[空位橫座標 + 1][空位縱座標] = 方塊[空位橫座標 + 1][空位縱座標], 方塊[空位橫座標][空位縱座標]
    elif 移動 == 右:
        方塊[空位橫座標][空位縱座標], 方塊[空位橫座標 - 1][空位縱座標] = 方塊[空位橫座標 - 1][空位縱座標], 方塊[空位橫座標][空位縱座標]


def 有效移動(方塊, 移動):
    空位橫座標, 空位縱座標 = 取得空位置(方塊)
    return (移動 == 上 and 空位縱座標 != len(方塊[0]) - 1) or \
        (移動 == 下 and 空位縱座標 != 0) or \
        (移動 == 左 and 空位橫座標 != len(方塊) - 1) or \
        (移動 == 右 and 空位橫座標 != 0)


def 取得隨機移動(方塊, 上一次移動=None):
    所有有效移動 = [上, 下, 左, 右]

    if 上一次移動 == 上 or not 有效移動(方塊, 下):
        所有有效移動.remove(下)
    if 上一次移動 == 下 or not 有效移動(方塊, 上):
        所有有效移動.remove(上)
    if 上一次移動 == 左 or not 有效移動(方塊, 右):
        所有有效移動.remove(右)
    if 上一次移動 == 右 or not 有效移動(方塊, 左):
        所有有效移動.remove(左)

    return random.choice(所有有效移動)


def 取得左上方塊座標(方塊橫座標, 方塊縱座標):
    左 = 邊框X座標 + (方塊橫座標 * 方塊尺寸) + (方塊橫座標 - 1)
    上方 = 邊框Y座標 + (方塊縱座標 * 方塊尺寸) + (方塊縱座標 - 1)
    return (左, 上方)


def 取得點擊座標(方塊, 橫座標, 縱座標):
    for 方塊橫座標 in range(len(方塊)):
        for 方塊縱座標 in range(len(方塊[0])):
            左, 上方 = 取得左上方塊座標(方塊橫座標, 方塊縱座標)
            tileRect = pygame.Rect(左, 上方, 方塊尺寸, 方塊尺寸)
            if tileRect.collidepoint(橫座標, 縱座標):
                return (方塊橫座標, 方塊縱座標)
    return (None, None)


def 畫方塊(方塊橫座標, 方塊縱座標, 數量, adjx=0, adjy=0):

    左, 上方 = 取得左上方塊座標(方塊橫座標, 方塊縱座標)
    pygame.draw.rect(顯示介面, 方塊顏色, (左 + adjx, 上方 + adjy, 方塊尺寸, 方塊尺寸))
    文字介面 = 基本字型.render(str(數量), True, 文字顏色)
    文字方格 = 文字介面.get_rect()
    文字方格.center = 左 + int(方塊尺寸 / 2) + adjx, 上方 + int(方塊尺寸 / 2) + adjy
    顯示介面.blit(文字介面, 文字方格)


def 製造文字(文字, 顏色, 背景顏色, 上方, 左):
    # create the Surface and Rect objects for some text.
    文字介面 = 基本字型.render(文字, True, 顏色, 背景顏色)
    文字方格 = 文字介面.get_rect()
    文字方格.topleft = (上方, 左)
    return (文字介面, 文字方格)


def 繪製畫面(方塊, 訊息):
    顯示介面.fill(背景顏色)
    if 訊息:
        文字介面, 文字方格 = 製造文字(訊息, 訊息顏色, 背景顏色, 5, 5)
        顯示介面.blit(文字介面, 文字方格)

    for 方塊橫座標 in range(len(方塊)):
        for 方塊縱座標 in range(len(方塊[0])):
            if 方塊[方塊橫座標][方塊縱座標]:
                畫方塊(方塊橫座標, 方塊縱座標, 方塊[方塊橫座標][方塊縱座標])

    左, 上方 = 取得左上方塊座標(0, 0)
    寬 = 行數 * 方塊尺寸
    高 = 列數 * 方塊尺寸
    pygame.draw.rect(顯示介面, 邊框顏色, (左 - 5, 上方 - 5, 寬 + 11, 高 + 11), 4)

    顯示介面.blit(重置介面, 重置方塊)
    顯示介面.blit(新介面, 新方塊)
    顯示介面.blit(解答畫面, 解答方塊)


def 移動動畫(方塊, 方向, 訊息, 動畫速度):

    空位橫座標, 空位縱座標 = 取得空位置(方塊)
    if 方向 == 上:
        橫向移動 = 空位橫座標
        縱向移動 = 空位縱座標 + 1
    elif 方向 == 下:
        橫向移動 = 空位橫座標
        縱向移動 = 空位縱座標 - 1
    elif 方向 == 左:
        橫向移動 = 空位橫座標 + 1
        縱向移動 = 空位縱座標
    elif 方向 == 右:
        橫向移動 = 空位橫座標 - 1
        縱向移動 = 空位縱座標

    # prepare the base surface
    繪製畫面(方塊, 訊息)
    基本介面 = 顯示介面.copy()

    移動左, 移動上方 = 取得左上方塊座標(橫向移動, 縱向移動)
    pygame.draw.rect(基本介面, 背景顏色, (移動左, 移動上方, 方塊尺寸, 方塊尺寸))

    for i in range(0, 方塊尺寸, 動畫速度):
        # animate the tile sliding over
        結束檢查()
        顯示介面.blit(基本介面, (0, 0))
        if 方向 == 上:
            畫方塊(橫向移動, 縱向移動, 方塊[橫向移動][縱向移動], 0, -i)
        if 方向 == 下:
            畫方塊(橫向移動, 縱向移動, 方塊[橫向移動][縱向移動], 0, i)
        if 方向 == 左:
            畫方塊(橫向移動, 縱向移動, 方塊[橫向移動][縱向移動], -i, 0)
        if 方向 == 右:
            畫方塊(橫向移動, 縱向移動, 方塊[橫向移動][縱向移動], i, 0)

        pygame.display.update()
        畫面更新控制器.tick(畫面更新率)


def 產生新題目(滑動次數):

    順序 = []
    方塊 = 區塊初始化()
    繪製畫面(方塊, '')
    pygame.display.update()
    pygame.time.wait(500) # pause 500 milliseconds for effect
    上一次移動 = None
    for i in range(滑動次數):
        移動 = 取得隨機移動(方塊, 上一次移動)
        移動動畫(方塊, 移動, 'Generating new puzzle... 產生新拼圖。', int(方塊尺寸 / 3))
        移動函式(方塊, 移動)
        順序.append(移動)
        上一次移動 = 移動
    return (方塊, 順序)


def 重置動畫(方塊, 移動記錄):

    記錄移動記錄 = 移動記錄[:]
    記錄移動記錄.reverse()

    for 移動 in 記錄移動記錄:
        if 移動 == 上:
            opposite移動 = 下
        elif 移動 == 下:
            opposite移動 = 上
        elif 移動 == 右:
            opposite移動 = 左
        elif 移動 == 左:
            opposite移動 = 右
        移動動畫(方塊, opposite移動, '', int(方塊尺寸 / 2))
        移動函式(方塊, opposite移動)


if __name__ == '__main__':
    main()
