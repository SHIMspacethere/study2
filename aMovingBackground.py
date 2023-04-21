# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 21:06:23 2023
filename :  [ECMEDU]/Python/Game/PyShooting/images/aMovingBackground.py
author: Dean Kim
Description :
        0.ShutingGame_v0412_2.py + Python_MariaDb_Ranking_03b.py 소스를 기초로 함
        
        1.움직이는 배경 구현 - 위에서 아래로 움직이게 한다.
          1) background_height = padHeight  # 움직이는 배경 변수 선언 ( dean )
    
          2) def initGame( ) : 에 아래 소스 추가
            (1) global background, background2  # 전역 변수 추가
            (2) # 움직이는 배경위한 소스추가( dean )
                background2 = backgound.copy() 
            
          3) def runGame( ) : 에 아래 소스 추가
             (1) global background, background2
             (2) # 전투기 초기 위치( x, y ) 아래에 소스 추가
                 background_y  = 0
                 background2_y = -background_height
             (3) drawObject( background, 0, 0 )  # 배경 화면 그리기 주석처리하고 아래 소스 추가
                 # drawObject( background, 0, 0 )  # 배경 화면 그리기
                 background_y += 2
                 background2_y += 2
                 
                 if ( background_y == background_height ) :
                     background_y = -background_height
                     
                 if ( background2_y == background_height ) :
                     background2_y = -background_height                     
                                  
                 drawObject( background,  0, background_y )
                 drawObject( background2, 0, background2_y )     
                
"""
"""
    pip install tk     
    pip install pymysql
    
    # 데이터베이스 생성
    CREATE DATABASE pythonDB;

    # 테이블 생성
    DROP TABLE IF EXISTS GameRankingTbl ;
    
    CREATE TABLE GameRankingTbl 
    (
        GR_NO    INT(11) NOT NULL AUTO_INCREMENT,
        GR_NAME  VARCHAR(100) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
        GR_SCORE INT(11) NULL DEFAULT NULL,
        GR_DATE  DATETIME NULL DEFAULT current_timestamp(),
        PRIMARY KEY (`GR_NO`) USING BTREE
    )
    COMMENT='슈팅게임 게임순위 테이블'
    COLLATE='utf8mb4_general_ci'
    ENGINE=InnoDB
    ;

"""
import pygame
import sys
import random
from time import sleep

BLACK = ( 0, 0, 0 )
padWidth = 480  # 게임화면의 가로크기
padHeight = 640  # 게임화면의 세로크기
background_height = padHeight  # 움직이는 배경 변수 선언 ( dean )
rockImage = [ 'rock01.png', 'rock02.png' ]
explosionSound = [ 'explosion01.wav', 'explosion02.wav', 'explosion03.wav', 'explosion04.wav' ]
screen = pygame.display.set_mode((padWidth, padHeight), pygame.DOUBLEBUF)

# 게임에 등장하는 객체를 드로잉
def drawObject( obj, x, y ) :
  global gamePad
  gamePad.blit( obj, ( x, y ) )
  
def initGame( ) :
  global gamePad, clock, background, fighter, missile, explosion, missileSound, gameOverSound, background, background2, shotcount
  pygame.init( )
  gamePad = pygame.display.set_mode( ( padWidth, padHeight ) )
  pygame.display.set_caption( 'PyShooting' )  # 게임 이름
  background = pygame.image.load( 'background.png' ) # 배경 그림
  
  # 움직이는 배경위한 소스추가( dean )
  background2 = background.copy()  
  
  fighter = pygame.image.load( 'fighter.png' ) # 전투기 그림
  missile = pygame.image.load( 'missile.png' )  # 미사일 그림
  explosion = pygame.image.load( 'explosion.png' )  # 폭발 그림
  pygame.mixer.music.load('music.wav')  # 배경음악
  pygame.mixer.music.play(-1)  # 배경음악 재상
  missileSound = pygame.mixer.Sound('missile.wav')  # 미사일 사운드
  gameOverSound = pygame.mixer.Sound('gameover.wav')  # 게임 오버 사운드
  clock = pygame.time.Clock( )

def runGame( ) :
  global gamePad, clock, background, fighter, missile, explosion, missileSound, shotCount, background, background2, shotcount
  
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
  
  # 움직이는 배경이미지을 위한 변수 선언( Dean )
  # 화면은 Top, Left 좌표는 (0,0)로 background2_y 는 0 아래쪽 마이너스 좌표에 위치해야 함
  background_y  = 0
  background2_y = -background_height   
  
  
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
        elif event.key == pygame.K_RIGHT :  # 전투기를 오른쪽으로 이동
          fighterX += 5
        elif event.key == pygame.K_UP :
          fighterY -= 5
        elif event.key == pygame.K_DOWN :
          fighterY += 5
        elif event.key == pygame.K_SPACE :  # 미사일 발사
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
    
    # 움직이는 배경 화면 좌표값 변경 ( dean )  
    background_y  += 2
    background2_y += 2
    
    if ( background_y == background_height ) :
        background_y =  -background_height
        
    if ( background2_y == background_height ) :
        background2_y = -background_height
        
    drawObject( background,  0, background_y )
    drawObject( background2, 0, background2_y )     
    # drawObject( background, 0, 0 )  # 배경 화면 그리기
    #-------------------------------------
    
        
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
        onGame = True   # 반복게임 중지(Dean)        
        continue
    
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
      gameOver( shotCount )     # 게임 랭킹 표시 추가 ( dean )
      onGame = True   # 반복게임 중지(Dean)    
      continue
      
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
  
# 게임 메시지 출력
def writeMessage( text ) :
    global gamePad, gameOverSound, shotCount
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
    game = Ranking() 
    game.showRanking( shotCount )    
    runGame()   # 주석처리( Dean )
    
# 전투기가 운석과 충돌했을 때 메시지 출력
def crash( ) :
    global gamePad
    writeMessage( '전투기 파괴!' )   
    
    #종료시 게임순위 및 등록 (Dean Class)    
    game = Ranking() 
    game.showRanking( shotCount )        
   
# 게임 오버 메시지 보이기
def gameOver( shotCount ) :    
    global gamePad
    writeMessage( '게임 오버!' )    
    
    # 랭킹 표시( Dean class)
    game = Ranking() 
    game.showRanking( shotCount )  
    # 무한 반복 게임 종료 ( Dean )

# Python_MariaDb_Ranking_03b.py    
from tkinter import *
    
class GameRanking :
    import pymysql
    
    #클래스 멤버 변수 정의
    conn = None
    curs = None 
    
    def __init__( self ) : 
        self.conn = None
        self.curs = None            
                     
    def __del__( self ) :                  
        del self      
        print( "class GameRanking 메모리 해제." )  
        
    
    # 게임점수가 랭킹에 포함되는지 체크
    def checkRanking( self, gameScore ) :
        import pymysql     
        rankingCnt = 5  # 보여줄 랭킹 갯수
        minScore = 0    # 랭킹순위중 가장 낮은 점수
        
        # MySQL Connection 연결
        self.conn = pymysql.connect( host='localhost', user='root', password='1234', db='pythonDB', charset='utf8' )    
         
        # Connection 으로부터 Dictoionary Cursor 생성
        self.curs = self.conn.cursor( pymysql.cursors.DictCursor )
         
        # SQL문 실행
        sql =  " Select IFNULL( MIN( a.gr_score ), 0 ) min_score, count(*) cnt From "
        sql += " (Select  gr_score  from gamerankingtbl order by gr_score desc LIMIT %s, %s ) a "           
                   
        self.curs.execute( sql, ( 0, rankingCnt ) )    # Top 5만 출력  
         
        # 데이타 Fetch
        rows = self.curs.fetchall()
        for row in rows:           
            minScore = row['min_score'] #    minScore 테이블 셀렉트한 첫번째 값 row[0] 입력
            cntRecord = row['cnt']      #    cntRecord 에 랭킹 총갯수
       
        # Connection 닫기
        self.conn.close()
     
        if ( gameScore > minScore or cntRecord < rankingCnt ) :    
            return True
        else:
            return False  
        
    ## 함수 선언부
    def addRankingToListBox( self ) :                      
        import pymysql             
        
        strData1, strData2, strData3, strData4  = [], [], [], []
        ranking = 1
        
        # MySQL Connection 연결
        self.conn = pymysql.connect(host='localhost', user='root', password='1234', db='pythonDB', charset='utf8')    
         
        # Connection 으로부터 Dictoionary Cursor 생성
        self.curs = self.conn.cursor( pymysql.cursors.DictCursor )
         
        # SQL문 실행            
        sql = " select gr_name, gr_score, gr_date from gamerankingtbl order by gr_score desc Limit %s, %s ;"
        self.curs.execute(sql, (0, 5))   # Top 5만 출력        
      
        # 데이타 Fetch
        rows = self.curs.fetchall()
        for row in rows:
         #   print(row)
            # 출력 : {'category': 1, 'id': 1, 'region': '서울', 'name': '김정수'}
            # print( row['gr_name'], row['gr_score'], row['gr_date'])
        
            strData1.append( ranking )
            strData2.append(row['gr_name']) # 리스트 strData1에 테이블 셀렉트한 첫번째 값 row[0] 입력
            strData3.append(row['gr_score'])
            strData4.append(row['gr_date'])
            ranking += 1
        
        # Connection 닫기
        self.conn.close()          
        
        return  strData1, strData2, strData3, strData4      
    
      
class Ranking( GameRanking ) :   
    window = None
     
    def __init__( self ) : 
         super().__init__()    
         window = None
   
    def __del__( self ) :                   
        del self      
        print( "sub class ShowRanking 메모리 해제."  )            

    # 저장 버튼 클릭시 호출되는 함수
    def insertRanking( self, gameScore, name ) :       
        from tkinter import messagebox
        import pymysql      
        
        data1, data2  = "", 0
        sql = ""   
       
        # entry(한줄텍스트박스)로 입력받은 값을 data 변수들에 입력       
        if ( gameScore > 0 ) :
             data2 = gameScore      # 점수           
        else:
             return
        
        # MySQL Connection 연결
        self.conn = pymysql.connect(host='localhost', user='root', password='1234', db='pythonDB', charset='utf8')    
         
        # Connection 으로부터 Dictoionary Cursor 생성
        self.curs = self.conn.cursor(pymysql.cursors.DictCursor)     
        
        sql = "insert into gamerankingtbl(gr_name,gr_score) values('" + name + "'," + str(data2) + ");"
        
        try :   # 예외처리 시작      
            print( sql )
            self.curs.execute( sql ) 
        except :    # 에러발생 시 작동
            messagebox.showerror('오류', '데이터 입력 오류가 발생함')
        else :  # 에러 없을 시 작동
            messagebox.showinfo('성공', '데이터 입력 성공')
           
        self.conn.commit()
        self.conn.close()
       
        # 추가한 리스트 새로고침       
        self.window.destroy()
        self.showRanking( gameScore )
        self.window.update()           
    
    def showRanking( self, gameScore ) :   
      
        ## 메인 코드부  
        BLACK = "#000000"
        WHITE = "#FFFFFF"
        GRAY  = "#CCCCCC" 
        
        #창을 화면 중앙에 배치
        self.window = Tk()
        
        win_x = 370   # 창 넓이
        win_y = 194   # 창 높이
        tot_x = self.window.winfo_screenwidth()
        tot_y = self.window.winfo_screenheight()
        x_pos = int( ( tot_x / 2 ) - ( win_x / 2 ) )
        y_pos = int( ( tot_y / 2 ) - ( win_y / 2 ) )
        
        self.window.geometry(f"{win_x}x{win_y}+{x_pos}+{y_pos}")
    
        self.window.resizable(width=False, height=False) # 창 크기 고정
        self.window.title("슈팅게임 순위 V0.3b")
        
        # 게임 점수가 Top 5에 속할 경우 등록 버튼 나오게 처리      
        padding_top = Label( self.window, text = "", width = 1, height = 1 )
        padding_top.grid( row = 0, column = 0, columnspan = 6 )        
               
        if ( self.checkRanking( gameScore ) ) :       
            padding_left = Label( self.window, text = "", width = 1 )
            padding_left.grid( row = 1, column = 0 ) 
            
            label =Label( self.window, text = "이름입력", fg=BLACK, bg = WHITE )
            label.grid( row = 1, column = 1 ) 
            
            edt1 = Entry( self.window, width = 17, bg = WHITE, justify = LEFT )  
            edt1.grid( row = 1, column = 2 )
            
            btnInsert = Button( self.window, text="저 장", bg = WHITE, justify = LEFT
                               ,command = lambda  : self.insertRanking ( gameScore, edt1.get() ) )                      
            btnInsert.grid( row = 1, column = 3 )
            
            msg = "게임점수는 " +str( gameScore )+"점"
            label =Label( self.window, text = msg , fg=BLACK, bg = WHITE )
            label.grid( row = 1, column = 4 ) 
        else :
            msg = "당신의 게임 점수는 " +str( gameScore )+"점입니다."
            label =Label( self.window, text = msg , fg=BLACK, bg = WHITE )
            label.grid( row = 1, column = 0, columnspan = 5 ) 
            
        
        padding_top = Label( self.window, text = "", width = 1, height = 1 )
        padding_top.grid( row = 2, column = 0, columnspan = 6 ) 
        
        padding_left = Label( self.window, text = "", width = 1 )
        padding_left.grid( row = 3, column = 0 ) 
        
        label =Label( self.window, text = "순위", width = 7, fg=WHITE, bg = BLACK, justify = LEFT )
        label.grid( row = 3, column = 1 ) 
        
        label =Label( self.window, text = "사용자 이름", width = 16, fg=WHITE, bg = BLACK, justify = LEFT )
        label.grid( row = 3, column = 2 ) 
        
        label =Label( self.window, text = "점 수", width = 5, fg=WHITE, bg = BLACK, justify = LEFT )
        label.grid( row = 3, column = 3 ) 
        
        label =Label( self.window, text = "날 짜", width = 16, fg=WHITE, bg = BLACK, justify = LEFT )
        label.grid( row = 3, column = 4 )
        
        padding_left = Label( self.window, text = "", width = 1 )
        padding_left.grid( row = 4, column = 0 ) 
        
        listData1 = Listbox( self.window, bg = 'white', width = 7, height = 5, justify = LEFT )
        listData1.grid( row = 4, column = 1 )
         
        listData2 = Listbox( self.window, bg = 'white', width = 17, height = 5, justify = LEFT )
        listData2.grid( row = 4, column = 2 )
        
        listData3 = Listbox( self.window, bg = 'white', width = 5, height = 5, justify = LEFT )
        listData3.grid( row = 4, column = 3 )
        
        listData4 = Listbox( self.window, bg = 'white', width = 17, height = 5, justify = LEFT )
        listData4.grid( row = 4, column = 4 )
        
        padding_right = Label( self.window, text = "", width = 1 )
        padding_right.grid( row = 4, column = 5 )      
        
        listData1.delete( 0, listData1.size() - 1 )    # 리스트박스에 있는 값들을 모두 지워버림
        listData2.delete( 0, listData2.size() - 1 )
        listData3.delete( 0, listData3.size() - 1 )    # 리스트박스에 있는 값들을 모두 지워버림
        listData4.delete( 0, listData4.size() - 1 )                      
                
        strDate1, strDate2, strData3, strDate4 = ( self.addRankingToListBox() )
      
        for item1, item2, item3, item4 in zip( strDate1, strDate2, strData3, strDate4 ): #item에 strData들을 한줄씩 입력
            listData1.insert(END, item1)    # 리스트박스 마지막줄에 item 값들을 넣어줘서 보여
            listData2.insert(END, item2) 
            listData3.insert(END, item3)  
            listData4.insert(END, item4)              
            
        self.window.mainloop()    
     

initGame( )
runGame( )