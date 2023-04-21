# -*- coding: utf-8 -*-
"""
  Created on Tue Apr 11 11:20:04 2023
  
  @PC user: 505-20
  
  FileName : ShootingGameEx.py
  Author   : David Bae
  Description : 슈팅 게임 예제
"""
import time
import pygame
import sys
import random
from time import sleep

BLACK = ( 0, 0, 0 )
padWidth = 480  # 게임화면의 가로크기
padHeight = 640  # 게임화면의 세로크기
rockImage = [ 'rock01.png', 'rock02.png', 'rock03.png', 'rock04.png', 'rock05.png', \
              'rock06.png', 'rock07.png', 'rock08.png', 'rock09.png', 'rock10.png', \
              'rock11.png', 'rock12.png', 'rock13.png', 'rock14.png', 'rock15.png', \
              'rock16.png', 'rock17.png', 'rock18.png', 'rock19.png', 'rock20.png', \
              'rock21.png', 'rock22.png', 'rock23.png', 'rock24.png', 'rock25.png', \
              'rock26.png', 'rock27.png', 'rock28.png', 'rock29.png', 'rock30.png' ]
explosionSound = [ 'explosion01.wav', 'explosion02.wav', 'explosion03.wav', ]
explosionSound = [ 'explosion01.wav', 'explosion02.wav', 'explosion03.wav', 'explosion04.wav' ]
screen = pygame.display.set_mode((padWidth, padHeight), pygame.DOUBLEBUF)

# 게임에 등장하는 객체를 드로잉
def drawObject( obj, x, y ) :
  global gamePad
  gamePad.blit( obj, ( x, y ) )
  
def initGame( ) :
  global gamePad, clock, background, fighter, missile, explosion, missileSound, gameOverSound
  pygame.init( )
  gamePad = pygame.display.set_mode( ( padWidth, padHeight ) )
  pygame.display.set_caption( 'PyShooting' )  # 게임 이름
  background = pygame.image.load( 'background.png' ) # 배경 그림
  fighter = pygame.image.load( 'fighter.png' ) # 전투기 그림
  missile = pygame.image.load( 'missile.png' )  # 미사일 그림
  explosion = pygame.image.load( 'explosion.png' )  # 폭발 그림
  pygame.mixer.music.load('music.wav')  # 배경음악
  pygame.mixer.music.play(-1)  # 배경음악 재생
  missileSound = pygame.mixer.Sound('missile.wav')  # 미사일 사운드
  gameOverSound = pygame.mixer.Sound('gameover.wav')  # 게임 오버 사운드
  clock = pygame.time.Clock( )

def runGame( ) :
  global gamePad, clock, background, fighter, missile, explosion, missileSound
  
  missileXY = []  # 무기 좌표 리스트
  
  # 운석 랜덤 생성
  rock = pygame.image.load( random.choice( rockImage ) ) 
  rockSize = rock.get_rect( ).size  # 운석크기
  rockWidth = rockSize[ 0 ]
  rockHeight = rockSize[ 1 ]
  destroySound = pygame.mixer.Sound( random.choice( explosionSound ) )
  
  # 운석 초기 위치 설정
  rockX = random.randrange( 0, ( padWidth - rockWidth ) )
  rockY = 0
  rockSpeed = 2
  
  # 전투기 크기
  fighterSize = fighter.get_rect().size
  fighterWidth = fighterSize[ 0 ]
  fighterHeight = fighterSize[ 1 ]
  
  # 전투기 초기 위치( x, y )
  x = padWidth * 0.45
  y = padHeight * 0.9
  fighterX = 0
  fighterY = 0
  
  # 전투기 미사일에 운석이 맞았을 경우 True
  isShot = False
  shotCount = 0
  rockPassed = 0
  
  onGame = False
  while not onGame :
    for event in pygame.event.get( ) :
      if event.type in [ pygame.QUIT ] :  # 게임 프로그램 종료
        pygame.quit( )
        sys.exit( )
        
      if event.type == pygame.KEYDOWN :
        if event.key == pygame.K_LEFT :  # 전투기를 왼쪽으로 이동
          fighterX -= 5
        if event.key == pygame.K_RIGHT :  # 전투기를 오른쪽으로 이동
          fighterX += 5
        if event.key == pygame.K_UP : # 위로 이동
          fighterY -= 5
        if event.key == pygame.K_DOWN : # 아래로 이동
          fighterY += 5
        if event.key == pygame.K_SPACE :  # 미사일 발사
          missileSound.play( )  # 미사일 사운드 재생
          missileX = x + fighterWidth/2
          missileY = y - fighterHeight
          missileXY.append( [ missileX, missileY ] )
          
      # 대각선 방향 이동 추가
      elif event.type == pygame.KEYUP :
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
          fighterX = 0
        elif event.key == pygame.K_UP or event.key == pygame.K_DOWN :
          fighterY = 0
          
      # 방향키를 떼면 전투기 점춤
      """
      if event.type in [ pygame.KEYUP ] :
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or \
            event.key == pygame.K_UP or event.key == pygame.K_DOWN :
          fighterX = 0
          fighterY = 0
      """
        
    drawObject( background, 0, 0 )  # 배경 화면 그리기
    
    x += fighterX
    if x < 0 :
      x = 0
    elif x > padWidth - fighterWidth :
      x = padWidth - fighterWidth
    
    y += fighterY
    if y < 0 :
      y = 0
    elif y > padHeight - fighterWidth :
      y = padHeight - fighterWidth
    
    # 전투기가 운석과 충돌했는지 체크
    if ( y < ( rockY + rockHeight ) ) :
      if ( ( rockX > x ) and ( rockX < ( x + fighterWidth ) ) ) or ( ( ( rockX + rockWidth ) > x ) and ( ( rockX + rockWidth ) < ( x + fighterWidth ) ) ) :
        crash()
    
    drawObject( fighter, x, y )  # 비행기를 게임 화면의 ( x, y ) 좌표에 그리기
    
    # 미사일 발사 화면에 그리기
    if len( missileXY ) != 0 :
      for i, bxy in enumerate( missileXY ) : # 미사일 요소에 대해 반복함
        bxy[ 1 ] -= 10  # 총알의 y좌표 -10 ( 위로 이동 )
        missileXY[ i ][ 1 ] = bxy[ 1 ]
        
        if bxy[ 1 ] < rockY :
          if bxy[ 0 ] > rockX and bxy[ 0 ] < rockX + rockWidth :
            missileXY.remove( bxy )
            isShot = True
            shotCount += 1
        
        if bxy[ 1 ] <= 0 :  # 미사일이 화면 밖을 벗어나면
          try :
            missileXY.remove( bxy )  # 미사일 제거
          except :
            pass
          
    if len( missileXY ) != 0 :
      for bx, by in missileXY :
        drawObject( missile, bx, by )
    
    # 운석 맞춘 점수 표시
    writeScore( shotCount )
    
    rockY += rockSpeed  # 운석 아래로 움직임
    
    # 운석이 지구로 떨어진 경우
    if rockY > padHeight :
      # 새로운 운석 ( 랜덤 )
      rock = pygame.image.load( random.choice( rockImage) ) 
      rockSize = rock.get_rect( ).size
      rockWidth = rockSize[ 0 ]
      rockHeight = rockSize[ 1 ]
      rockX = random.randrange( 0, padWidth - rockWidth )
      rockY = 0
      rockPassed += 1
    
    if rockPassed == 3 : # 운석 3개 놓치면 게임오버
      gameOver( )
      
    # 놓친 운석 수 표시
    writePassed( rockPassed )
    
    #  운석을 맞춘 경우
    if isShot :  
      # 운석 폭발
      drawObject( explosion, rockX, rockY )  # 운석 폭발 그리기
      destroySound.play( )  # 운석 폭발 사운드 재생
      
      # 새로운 운석( 랜덤 )
      rock = pygame.image.load( random.choice( rockImage ) )
      rockSize = rock.get_rect( ).size
      rockWidth = rockSize[ 0 ]
      rockHeight = rockSize[ 1 ]
      rockX = random.randrange( 0, padWidth - rockWidth )
      rockY = 0
      destroySound = pygame.mixer.Sound( random.choice( explosionSound ) )
      isShot = False
      
      # 운석 맞추면 속도 증가
      rockSpeed += 0.02
      if rockSpeed >= 10 :
          rockSpeed = 10
    
    drawObject( rock, rockX, rockY )  # 운석 그리기
        
    pygame.display.update( )  # 게임 화면을 다시 그림
    
    gamePad.fill( BLACK )  # 게임 화면 ( 검은색 )
    
    #pygame.display.update( )  # 게임화면을 다시 그림
    
    clock.tick( 60 )  # 게임화면의 초당 프레임수를 60으로 설정
    
  pygame.quit( )  # pygame 종료
  
# 운석을 맞춘 개수 계산
def writeScore( count ) :
  global gamePad
  font = pygame.font.Font( 'NanumGothic.ttf', 20 )
  text = font.render( '파괴한 운석 수 :' + str( count ), True, ( 255, 255, 255 ) )
  gamePad.blit( text, (10, 0 ) )
  
# 운석이 화면 아래로 통과한 개수
def writePassed( count ) :
  global gamePad
  font = pygame.font.Font( 'NanumGothic.ttf', 20 )
  text = font.render( '놓친 운석 :' + str( count ), True, ( 255, 255, 255 ) )
  gamePad.blit( text, (360, 0 ) )

# 첫 화면( 시놉시스 ) 구현
def runStory( ) :
  global gamePad, background, screen  
  screen_width = 480  # 게임화면의 가로크기
  screen_height = 640  # 게임화면의 세로크기
  drawObject( background, 0, 0 )  # 배경 화면 그리기
  
  # 한국 글씨 폰트 적용
  font_path = './font/12Bold.ttf'
  font_size = 30
  korean_font = pygame.font.Font(font_path, font_size)
  
  
  # 시놉시스
  text_lines = ["미래의 지구,", "외계인의 침공이", "시작되었다.", "외계인은", "이미 지구 내에", "깊숙이 침투했고", "전 인류는 ", "모든 기술력을 모아 ", "‘STEP-1호기’를 ", "완성하고 마는데...", "‘STEP-1호기’로 ", "지구 안에 침투한 ", "외계인들을 ", "모두 물리치자."]
  text_positions = [(screen_width // 2, screen_height + korean_font.get_height() * i) for i in range(len(text_lines))]
  text_speed = 1
  
  # 프레임 조정을 위한 시간 추가
  clock = pygame.time.Clock()
  
  # 키를 받아 종료하기 전까지 글씨 올라감
  while True:
      # 끄면 종료됨
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
              quit()
              
      # 배경을 우주 이미지로 띄워줌
      drawObject( background, 0, 0 )
  
      # 글씨의 위치 지정
      for i, position in enumerate(text_positions):
          x, y = position
          y -= text_speed
          text_positions[i] = (x, y)
  
      # 화면에 글씨 표현
      for i, line in enumerate(text_lines):
          text = korean_font.render(line, True, (255, 255, 255))
          x, y = text_positions[i]
          screen.blit(text, (x - text.get_width() // 2, y))
  
      # 화면 업데이트
      pygame.display.update()
  
      # 화면 프레임 정해주기
      clock.tick(60)
      
      # 아무키나 누르면 runMenu( ) 호
      for event in pygame.event.get( ) :
        if event.type in [ pygame.QUIT ] : 
          pygame.quit( )
          sys.exit( )
        if event.type == pygame.KEYDOWN :  
          runMenu( )
          
# 시작화면 출력
def runMenu( ) :
    global gamePad, background
    drawObject( background, 0, 0 )  # 배경 화면 그리기
    text = 'press any key'
    textfont = pygame.font.Font( 'NanumGothic.ttf', 80 )
    text = textfont.render( text, True, ( 255, 0, 0 ) )
    textpos = text.get_rect( )
    textpos.center = ( padWidth / 2, padHeight / 2 )
    gamePad.blit( text, textpos )
    pygame.display.update( )
    while True :
      for event in pygame.event.get( ) :
        if event.type in [ pygame.QUIT ] :  # 게임 프로그램 종료
          pygame.quit( )
          sys.exit( )
        if event.type == pygame.KEYDOWN :
          runGame( )
    
# 게임 메시지 출력
def writeMessage( text ) :
    global gamePad, gameOverSound, background
    textfont = pygame.font.Font( 'NanumGothic.ttf', 80 )
    text = textfont.render( text, True, ( 255, 0, 0 ) )
    textpos = text.get_rect( )
    textpos.center = ( padWidth / 2, padHeight / 2 )
    gamePad.blit( text, textpos )
    pygame.display.update( )
    pygame.mixer.music.stop()  # 배경 음악 정지
    gameOverSound.play()  # 게임 오버 사운드 재생
    sleep( 2 )
    pygame.mixer.music.play( -1 )
    runMenu( )
    
# 전투기가 운석과 충돌했을 때 메시지 출력
def crash( ) :
    global gamePad, background
    writeMessage( '전투기 파괴!' )
    
# 게임 오버 메시지 보이기
def gameOver( ) :
    global gamePad, background
    writeMessage( '게임 오버!' )
  
initGame( )
runStory( )
runGame( )