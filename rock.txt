
import time
import pygame
import sys
import random
from time import sleep

BLACK = ( 0, 0, 0 )
padWidth = 480  # 게임화면의 가로크기
padHeight = 640  # 게임화면의 세로크기
background_height = padHeight  # 움직이는 배경 변수 선언 
rockImage = [ 'rock01.png', 'rock02.png', 'rock03.png', 'rock04.png', 'rock05.png', \
              'rock06.png', 'rock07.png', 'rock08.png', 'rock09.png', 'rock10.png', \
              'rock11.png', 'rock12.png', 'rock13.png', 'rock14.png', 'rock15.png', \
              'rock16.png', 'rock17.png', 'rock18.png', 'rock19.png', 'rock20.png', \
              'rock21.png', 'rock22.png', 'rock23.png', 'rock24.png', 'rock25.png', \
              'rock26.png', 'rock27.png', 'rock28.png', 'rock29.png', 'rock30.png' ]
explosionSound = [ 'explosion01.wav', 'explosion02.wav', 'explosion03.wav', ]
explosionSound = [ 'explosion01.wav', 'explosion02.wav', 'explosion03.wav', 'explosion04.wav' ]
screen = pygame.display.set_mode((padWidth, padHeight), pygame.DOUBLEBUF)
window_size = ( padWidth, padHeight )
rock_list = []

def drawObject( obj, x, y ) :
  global gamePad
  gamePad.blit( obj, ( x, y ) )

def initGame( ) :
  global gamePad, clock, background, background2, fighter, missile, explosion, missileSound, gameOverSound
  pygame.init( )
  gamePad = pygame.display.set_mode( ( padWidth, padHeight ) )
  pygame.display.set_caption( 'PyShooting' )  # 게임 이름
  background = pygame.image.load( 'background1.png' )  # 배경 그림 1, 2, 3
  background2 = background.copy()  # 움직이는 배경위한 소스추가
  fighter = pygame.image.load( 'fighter.png' ) # 전투기 그림
  missile = pygame.image.load( 'missile.png' )  # 미사일 그림
  explosion = pygame.image.load( 'explosion.png' )  # 폭발 그림
  pygame.mixer.music.load('music.wav')  # 배경음악
  pygame.mixer.music.play(-1)  # 배경음악 재생
  missileSound = pygame.mixer.Sound('missile.wav')  # 미사일 사운드
  gameOverSound = pygame.mixer.Sound('gameover.wav')  # 게임 오버 사운드
  clock = pygame.time.Clock( )

def runGame( ) :
  global gamePad, clock, background, background2, fighter, missile, explosion, missileSound
  missileXY = []  # 무기 좌표 리스트
  gaugeWidth = 100
  gaugeHeight = 10
  gaugeX = padWidth / 2 - gaugeWidth / 2
  gaugeY = padHeight - gaugeHeight - 10
  gaugeValue = 0
  rock = pygame.image.load( random.choice( rockImage ) ).convert_alpha()
  rockSize = rock.get_rect( ).size  # 운석크기
  rockWidth = rockSize[ 0 ]
  rockHeight = rockSize[ 1 ]
  destroySound = pygame.mixer.Sound( random.choice( explosionSound ) )
  rockX = random.randrange( 0, ( padWidth - rockWidth ) )
  rockY = 0
  rockSpeed = 2
  rockAngle = 0 
  rockDirection = random.choice([-1, 1])  # Randomly select initial horizontal direction (-1 for left, 1 for right)
  fighterSize = fighter.get_rect().size
  fighterWidth = fighterSize[ 0 ]
  fighterHeight = fighterSize[ 1 ]
  x = padWidth * 0.45
  y = padHeight * 0.9
  fighterX = 0
  fighterY = 0
  background_y  = 0
  background2_y = -background_height
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
        if event.key == pygame.K_q:   # q 눌렀을 때 모든 운석 없애기
          isShot = True
          shotCount += 1
      elif event.type == pygame.KEYUP :
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
          fighterX = 0
        elif event.key == pygame.K_UP or event.key == pygame.K_DOWN :
          fighterY = 0
    background_y  += 0.2
    background2_y += 0.2
    if ( background_y == background_height ) :
        background_y =  -background_height
    if ( background2_y == background_height ) :
        background2_y = -background_height
    drawObject( background,  0, background_y )
    drawObject( background2, 0, background2_y )     
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
    if ( ( rockY + rockHeight >= y ) and ( rockY <= y + fighterHeight ) and ((rockX >= x and rockX <= x + fighterWidth) or (rockX + rockWidth >= x and rockX + rockWidth <= x + fighterWidth))) :
        crash()
    drawObject( fighter, x, y )  # 비행기를 게임 화면의 ( x, y ) 좌표에 그리기
    rock = pygame.image.load( random.choice( rockImage ) ).convert_alpha()
    rockSize = rock.get_rect( ).size  # 운석크기
    rockWidth = rockSize[ 0 ]
    rockHeight = rockSize[ 1 ]
    if len(rock_list) < 10:
        if random.randint(0, 50) == 0:
            rockX = random.randint(0, window_size[0] - rockWidth)
            rockY = rockHeight
            rock_speed = random.randint(1, 5)
            rock_list.append((rockX, rockY, rock_speed))  
    for i, rock in enumerate(rock_list):
        rockX, rockY, rock_speed = rock
        rockY += rock_speed
        rock_list[i] = (rockX, rockX, rock_speed)
        if rockY > window_size[1]:
            rock_list.pop(i)
    for rock in rock_list:
        rockX, rockY, rock_speed = rock
        screen.blit(rockImage, (rockX, rockY))
    pygame.display.update()
    for rock in rock_list:
        if rock[1] > window_size[1]:
            score += 1
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
    writeScore( shotCount )
    rockY += rockSpeed  # 운석 아래로 움직임
    if rockY > padHeight :
      rock = pygame.image.load( random.choice( rockImage) ) 
      rockSize = rock.get_rect( ).size
      rockWidth = rockSize[ 0 ]
      rockHeight = rockSize[ 1 ]
      rockX = random.randrange( 0, padWidth - rockWidth )
      rockY = 0
      rockPassed += 1
    if rockPassed == 3 : # 운석 3개 놓치면 게임오버
      gameOver( )
    writePassed( rockPassed )
    if isShot :  
      drawObject( explosion, rockX, rockY )  # 운석 폭발 그리기
      destroySound.play( )  # 운석 폭발 사운드 재생
      rock = pygame.image.load( random.choice( rockImage ) )
      rockSize = rock.get_rect( ).size
      rockWidth = rockSize[ 0 ]
      rockHeight = rockSize[ 1 ]
      rockX = random.randrange( 0, padWidth - rockWidth )
      rockY = 0
      destroySound = pygame.mixer.Sound( random.choice( explosionSound ) )
      isShot = False
      gaugeValue += 10
      if gaugeValue > 100 :
          gaugeValue = 100
      # 운석 맞추면 속도 증가
      rockSpeed += 0.02
      if rockSpeed >= 10 :
          rockSpeed = 10
    pygame.draw.rect(gamePad, (255, 0, 0), (gaugeX, gaugeY, gaugeWidth, gaugeHeight), border_radius=3)  # Red gauge bar
    pygame.draw.rect(gamePad, (0, 255, 0), (gaugeX, gaugeY, gaugeWidth * (gaugeValue / 100), gaugeHeight), border_radius=50)  # Green gauge bar based on gaugeValue
    useSkill(gaugeValue) 
    pygame.display.update( )  # 게임 화면을 다시 그림
    gamePad.fill( BLACK )  # 게임 화면 ( 검은색 )
    clock.tick( 60 )  # 게임화면의 초당 프레임수를 60으로 설정
  pygame.quit( )  # pygame 종료
def useSkill ( gaugeValue ) :
  global gamePad
  font = pygame.font.Font( 'NanumGothic.ttf', 20 )
  text = font.render('skill gauge' , True ,(255, 255, 255) )
  gamePad.blit( text, (190,590))
def writeScore( count ) :
  global gamePad
  font = pygame.font.Font( 'NanumGothic.ttf', 20 )
  text = font.render( '파괴한 운석 수 :' + str( count ), True, ( 255, 255, 255 ) )
  gamePad.blit( text, (10, 0 ) )
def writePassed( count ) :
  global gamePad
  font = pygame.font.Font( 'NanumGothic.ttf', 20 )
  text = font.render( '놓친 운석 :' + str( count ), True, ( 255, 255, 255 ) )
  gamePad.blit( text, (360, 0 ) )
def runStory( ) :
  global gamePad, background, screen  
  screen_width = 480  # 게임화면의 가로크기
  screen_height = 640  # 게임화면의 세로크기
  drawObject( background, 0, 0 )  # 배경 화면 그리기
  font_path = './font/12Bold.ttf'
  font_size = 30
  korean_font = pygame.font.Font(font_path, font_size)
  text_lines = ["미래의 지구,", "외계인의 침공이", "시작되었다.", "외계인은", "이미 지구 내에", "깊숙이 침투했고", "전 인류는 ", "모든 기술력을 모아 ", "‘STEP-1호기’를 ", "완성하고 마는데...", "‘STEP-1호기’로 ", "지구 안에 침투한 ", "외계인들을 ", "모두 물리치자."]
  text_positions = [(screen_width // 2, screen_height + korean_font.get_height() * i) for i in range(len(text_lines))]
  text_speed = 1
  clock = pygame.time.Clock()
  while True:
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
              quit()
      drawObject( background, 0, 0 )
      for i, position in enumerate(text_positions):
          x, y = position
          y -= text_speed
          text_positions[i] = (x, y)
      for i, line in enumerate(text_lines):
          text = korean_font.render(line, True, (255, 255, 255))
          x, y = text_positions[i]
          screen.blit(text, (x - text.get_width() // 2, y))
      pygame.display.update()
      clock.tick(60)
      for event in pygame.event.get( ) :
        if event.type in [ pygame.QUIT ] : 
          pygame.quit( )
          sys.exit( )
        if event.type == pygame.KEYDOWN :  
          runMenu( )
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
def writeMessage( text ) :
    global gamePad, gameOverSound
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
def crash( ) :
    global gamePad
    writeMessage( '전투기 파괴!' )
def gameOver( ) :
    global gamePad
    writeMessage( '게임 오버!' )
initGame( )
runStory( )
runGame( )