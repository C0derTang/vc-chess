import speech_recognition as sr
import pyautogui as pag

from time import sleep

r = sr.Recognizer()
board = [[None]*8 for _ in range(8)]

def matrixflip(m,d):
    tempm = m.copy()
    if d=='h':
        for i in range(0,len(tempm),1):
                tempm[i].reverse()
    elif d=='v':
        tempm.reverse()
    return(tempm)

def calibrate_board():
    print('Position cursor on top left rook')
    sleep(3)
    topcorner = pag.position()
    print('Position cursor on bottom right rook')
    sleep(3)
    bottomcorner = pag.position()
    print('Calibration complete!')
    print(topcorner.x, bottomcorner.x)
    width = bottomcorner.x - topcorner.x
    height = topcorner.y - bottomcorner.y

    for i in range(8):
        for j in range(8):
            board[i][j] = (topcorner.x + i*width/7, bottomcorner.y + j*height/7)
    print(board)

def get_color():
    color = ''
    while color != 'black' and color != 'white':
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration = 2)
            r.pause_threshold = 1
            print("What color are you playing?")
            audio = r.listen(source)
            try:
                print('Recognizing')
                query = r.recognize_google(audio, language = 'en-in')
                color =  query.lower()
            except:
                print('Unable to Recognize')
    print('you are playing', color)
    return color

def move_piece():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration = 2)
        r.pause_threshold = 1
        print("Make your move:")
        audio = r.listen(source)
        try:
            print('Recognizing')
            query = r.recognize_google(audio, language = 'en-in')
            return query.lower()
        except:
            print('Unable to Recognize')
            return ""

def parse_input(text):
    move1 = text.split()[0]
    move2 = text.split()[2]
    if move1[0] not in 'abcdefgh' or move2[0] not in 'abcdefgh' or move1[1] not in '12345678' or move2[1] not in '12345678':
        return False
    move1 = (ord(move1[0]) - 97, int(move1[1])-1)
    move2 = (ord(move2[0]) - 97, int(move2[1])-1)
    print(text)
    print(move1, move2)
    pag.click(board[move1[0]][move1[1]])
    pag.click(board[move2[0]][move2[1]])
    return True

calibrate_board()
color = get_color()
if color == 'white':
    pass
else:
    board = (matrixflip(board, 'v'))
    board = (matrixflip(board, 'h'))
while True:
    chosen = move_piece()
    if len(chosen.split()) != 3:
        continue
    parse_input(chosen)
    
    print(chosen)
