#-------------------------------------------------------------------------------
# Name:        pygame_tc.py
# Purpose:
#
# Author:      renyuan
#
# Created:     31/05/2014
# Copyright:   (c) renyuan 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pygame
import sys, random, copy

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
