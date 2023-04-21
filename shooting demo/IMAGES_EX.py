# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 15:00:41 2023

@author: psb20
"""

import pygame
import os
import sys
import random
from time import sleep

pygame.init( ) #초기화


fighter_X = 200
fighter_Y = 400

size = [ 1000,1000 ]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("이미지 애니메이션")

#키누른상태
Move_right = False
Move_left = False

#무브에 대한 카운터
moveCount = 0

#오른쪽 임직일때 이미지 리스트
right_Move = [ pygame.image.load( "fighter-R002R.png" ), pygame.image.load( "fighter-R003R.png" ), \
               pygame.image.load( "fighter-R004R.png" ), pygame.image.load( "fighter-R005R.png" ), \
               pygame.image.load( "fighter-R006R.png" ), pygame.image.load( "fighter-R007R.png" ), \
               pygame.image.load( "fighter-R008R.png" ), pygame.image.load( "fighter-R009R.png" ), \
               pygame.image.load( "fighter-R009R.png" ), pygame.image.load( "fighter-R009R.png" ), \
               pygame.image.load( "fighter-R009R.png" ), pygame.image.load( "fighter-R009R.png" ), \
               pygame.image.load( "fighter-R009R.png" ), pygame.image.load( "fighter-R009R.png" ), \
               pygame.image.load( "fighter-R009R.png" ), pygame.image.load( "fighter-R009R.png" ), \
               pygame.image.load( "fighter-R009R.png" ), pygame.image.load( "fighter-R009R.png" ), \
               pygame.image.load( "fighter-R009R.png" ), pygame.image.load( "fighter-R009R.png" ), \
               pygame.image.load( "fighter-R009R.png" ), pygame.image.load( "fighter-R009R.png" ), \
               pygame.image.load( "fighter-R009R.png" ), pygame.image.load( "fighter-R009R.png" ), \
               pygame.image.load( "fighter-R009R.png" ), pygame.image.load( "fighter-R009R.png" ), \
               pygame.image.load( "fighter-R009R.png" ), pygame.image.load( "fighter-R009R.png" ), \
               pygame.image.load( "fighter-R009R.png" ), pygame.image.load( "fighter-R009R.png" ), \
               pygame.image.load( "fighter-R009R.png" ), pygame.image.load( "fighter-R009R.png" ), \
               pygame.image.load( "fighter-R009R.png" ), pygame.image.load( "fighter-R009R.png" ), \
               pygame.image.load( "fighter-R009R.png" ), pygame.image.load( "fighter-R009R.png" ), \
               pygame.image.load( "fighter-R009R.png" ), pygame.image.load( "fighter-R009R.png" ), \
               pygame.image.load( "fighter-R009R.png" ), pygame.image.load( "fighter-R009R.png" ), \
               pygame.image.load( "fighter-R009R.png" ), pygame.image.load( "fighter-R009R.png" ), \
               pygame.image.load( "fighter-R009R.png" ), pygame.image.load( "fighter-R009R.png" ), \
               pygame.image.load( "fighter-R009R.png" ), pygame.image.load( "fighter-R009R.png" ), \
               pygame.image.load( "fighter-R009R.png" ), pygame.image.load( "fighter-R009R.png" ), \
               pygame.image.load( "fighter-R009R.png" ), pygame.image.load( "fighter-R009R.png" ), \
               pygame.image.load( "fighter-R009R.png" ), pygame.image.load( "fighter-R009R.png" ), \
               pygame.image.load( "fighter-R009R.png" ), pygame.image.load( "fighter-R009R.png" ), \
               pygame.image.load( "fighter-R009R.png" ), pygame.image.load( "fighter-R009R.png" ), ]
    
    
left_Move = [  pygame.image.load( "fighter-L002R.png" ), pygame.image.load( "fighter-L003R.png" ), \
               pygame.image.load( "fighter-L004R.png" ), pygame.image.load( "fighter-L005R.png" ), \
               pygame.image.load( "fighter-L006R.png" ), pygame.image.load( "fighter-L007R.png" ), \
               pygame.image.load( "fighter-L008R.png" ), pygame.image.load( "fighter-L009R.png" ), \
               pygame.image.load( "fighter-L009R.png" ), pygame.image.load( "fighter-L009R.png" ), \
               pygame.image.load( "fighter-L009R.png" ), pygame.image.load( "fighter-L009R.png" ), \
               pygame.image.load( "fighter-L009R.png" ), pygame.image.load( "fighter-L009R.png" ), \
               pygame.image.load( "fighter-L009R.png" ), pygame.image.load( "fighter-L009R.png" ), \
               pygame.image.load( "fighter-L009R.png" ), pygame.image.load( "fighter-L009R.png" ), \
               pygame.image.load( "fighter-L009R.png" ), pygame.image.load( "fighter-L009R.png" ), \
               pygame.image.load( "fighter-L009R.png" ), pygame.image.load( "fighter-L009R.png" ), \
               pygame.image.load( "fighter-L009R.png" ), pygame.image.load( "fighter-L009R.png" ), \
               pygame.image.load( "fighter-L009R.png" ), pygame.image.load( "fighter-L009R.png" ), \
               pygame.image.load( "fighter-L009R.png" ), pygame.image.load( "fighter-L009R.png" ), \
               pygame.image.load( "fighter-L009R.png" ), pygame.image.load( "fighter-L009R.png" ), \
               pygame.image.load( "fighter-L009R.png" ), pygame.image.load( "fighter-L009R.png" ), \
               pygame.image.load( "fighter-L009R.png" ), pygame.image.load( "fighter-L009R.png" ), \
               pygame.image.load( "fighter-L009R.png" ), pygame.image.load( "fighter-L009R.png" ), \
               pygame.image.load( "fighter-L009R.png" ), pygame.image.load( "fighter-L009R.png" ), \
               pygame.image.load( "fighter-L009R.png" ), pygame.image.load( "fighter-L009R.png" ), \
               pygame.image.load( "fighter-L009R.png" ), pygame.image.load( "fighter-L009R.png" ), \
               pygame.image.load( "fighter-L009R.png" ), pygame.image.load( "fighter-L009R.png" ), \
               pygame.image.load( "fighter-L009R.png" ), pygame.image.load( "fighter-L009R.png" ), \
               pygame.image.load( "fighter-L009R.png" ), pygame.image.load( "fighter-L009R.png" )]

stand_Image = pygame.image.load( "fighter-001R.png" )

#플래이어 움직이는 애니메이션 함수
def fighterMove( ) :
    global moveCount, fighter_X, fighter_Y
    
    screen.fill( ( 150, 150, 150 ) ) # 배경이 색을 칠한다. 그려진 이미지를 지우기 위함

    if ( moveCount > 100 ) :
        moveCount = 0
            
    #만약 오른쪽키나 오니쪽키를 눌렀을 때 애니메이션 리스트에 있는 이미지를 그려줌.
    #그리고 walkCount가 +1 더해져서 요소마다 바뀐 이미지가 그려짐.
    if Move_left == True :
        screen.blit( left_Move[moveCount], ( fighter_X, fighter_Y ) )
        moveCount +=1
    elif Move_right == True :
        screen.blit( right_Move[moveCount], ( fighter_X, fighter_Y ) )
        moveCount +=1
    
    else : #가만히 있으령우 stand Image 그려짐.
        screen.blit( stand_Image, ( fighter_X, fighter_Y ) )
        
        
clock = pygame.time.Clock( )

while True :
        clock.tick( 30 )
        
        for event in pygame.event.get( ) :
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_RIGHT :
                    Move_right = True
                    Move_left = False
                if event.key == pygame.K_LEFT :
                    Move_left = True
                    Move_right = False
                    
            if event.type == pygame.KEYUP :
                if event.key == pygame.K_RIGHT :
                    Move_right = False
                    Move_left = False
                if event.key == pygame.K_LEFT :
                    Move_left = False
                    Move_right = False
        while True:
              # 끄면 종료됨
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    
                    
        # 오른쪽 상태가 True인 경우 플레이어 표지션 이동
        if Move_right == True :
            fighter_X += 10
    
    # 오른쪽 상태가 True인 경우 플레이어 포지션 이동
        elif Move_left == True :
            fighter_X -= 10
    
    # 아무것도 누르지 않으면 moveCount 초기화
    
        else :
            moveCount = 0
            
        fighterMove( ) 
        pygame.display.update( )
        
        
pygame.quit( )