from tkinter import *
from tkinter import ttk, messagebox
import random

def create_snake():
    snake.append(canvas.create_rectangle(snakeSize,snakeSize, snakeSize * 2, snakeSize * 2, fill="white"))

def overlapping(a, b):
    if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
        return True
    return False

def growSnake():
    lastElement = len(snake)-1
    lastElementPos = canvas.coords(snake[lastElement])
    snake.append(canvas.create_rectangle(0,0, snakeSize,snakeSize,fill="#FDF3F3"))
    if (direction == "left"):
        canvas.coords(snake[lastElement+1],lastElementPos[0]+snakeSize,
                        lastElementPos[1],lastElementPos[2]+snakeSize,lastElementPos[3])
    if (direction == "right"):
        canvas.coords(snake[lastElement+1],lastElementPos[0]-snakeSize,
                        lastElementPos[1],lastElementPos[2]-snakeSize,lastElementPos[3])
    if (direction == "up"):
        canvas.coords(snake[lastElement+1],lastElementPos[0],
                        lastElementPos[1]+snakeSize,lastElementPos[2],lastElementPos[3]+snakeSize)
    else:
        canvas.coords(snake[lastElement+1],lastElementPos[0],
                        lastElementPos[1]-snakeSize,lastElementPos[2],lastElementPos[3]-snakeSize)
    global score, highestscore
    score += 10
    highestscore = []
    with open("score.txt", "r") as scoresheet:
        highestscore.append(scoresheet.read())
        highestscore = ''.join(highestscore)
        if score > int(highestscore):
            wow = canvas.create_text(300, 20, font='Terminal 10 bold', text='You beat previous\n   high score', fill='white', anchor=N)
            highest = score     
            with open("score.txt", "w") as highest:
                highest.write(str(score))
    txt = str(score)
    canvas.itemconfigure(scoreText, text=txt)

def moveFood():
    global food, foodX, foodY, pic
    canvas.move(food, (foodX*(-1)), (foodY*(-1)))
    canvas.move(pic, (foodX*(-1)), (foodY*(-1)))
    foodX = random.randint(0,width-snakeSize)
    foodY = random.randint(0,height-snakeSize)
    canvas.move(food, foodX, foodY)
    canvas.move(pic, foodX, foodY)

def moveSnake():
    global positions
    if run:
        positions = []
        positions.append(canvas.coords(snake[0]))
        if positions[0][0] < 0:
            canvas.coords(snake[0],width,positions[0][1],width-snakeSize,positions[0][3])
        elif positions[0][2] > width:
            canvas.coords(snake[0],0-snakeSize,positions[0][1],0,positions[0][3])
        elif positions[0][3] > height:
            canvas.coords(snake[0],positions[0][0],0-snakeSize,positions[0][2],0)
        elif positions[0][1] < 0:
            canvas.coords(snake[0],positions[0][0],height,positions[0][2],height-snakeSize)
        positions.clear()
        positions.append(canvas.coords(snake[0]))
        if direction == "left":
            canvas.move(snake[0], -snakeSize,0)
        elif direction == "right":
            canvas.move(snake[0], snakeSize,0)
        elif direction == "up":
            canvas.move(snake[0], 0,-snakeSize)
        elif direction == "down":
            canvas.move(snake[0], 0,snakeSize)
        sHeadPos = canvas.coords(snake[0])
        foodPos = canvas.coords(food)
        if overlapping(sHeadPos, foodPos):
            moveFood()
            growSnake()
        for i in range(1, len(snake)):
            if overlapping(sHeadPos, canvas.coords(snake[i])):
                gameOver = True 
                game_Over()  
        for i in range(1, len(snake)):
            positions.append(canvas.coords(snake[i]))
        for i in range(len(snake)-1):
                canvas.coords(snake[i+1],positions[i][0],
                                positions[i][1],positions[i][2],positions[i][3])
        if 'gameOver' not in locals():
            window.after(speed, moveSnake)

def game_Over():
    canvas.unbind('<space>') 
    canvas.create_text(302, 200, font='Terminal 50 bold', text='GAME OVER', fill='white')
    buttonrestart = Button(canvas, image=gameover_restart, command= restart, borderwidth=0,background="#6ac092")
    canvas.create_window(180, 250, window=buttonrestart, anchor="nw")
    buttonmainmenu = Button(canvas, image=gameover_home, command= mainmenu, borderwidth=0, background="#6ac092")
    canvas.create_window(265, 250, window=buttonmainmenu, anchor="nw")
    buttonexit = Button(canvas, image=gameover_exit, command= window.destroy, borderwidth=0, background="#6ac092")
    canvas.create_window(350, 250, window=buttonexit, anchor="nw")        
    if score > int(highestscore):
        with open ("highest_score_list.txt", "a") as king:
            king.write(e.get() + " " + str(score) + "\n") 
    
def placeFood():
    global food, foodX, foodY, pic, score
    food = canvas.create_rectangle(0,0, 20, 20, fill="", outline="")
    foodX = random.randint(0,width-snakeSize)
    foodY = random.randint(0,height-snakeSize)
    canvas.move(food, foodX, foodY)
    pic = canvas.create_image(0, 0, image=food_pic, anchor= NW)
    canvas.move(pic, foodX, foodY )

def leftKey(event):
    global direction
    direction = "left"
def rightKey(event):
    global direction
    direction = "right"
def upKey(event):
    global direction
    direction = "up"
def downKey(event):
    global direction
    direction = "down"

def setWindowDimensions(w,h):
    window.title("Snake Game")
    window.iconbitmap("snake_ICON.ico")
    window.geometry("600x600")
    return window

def Scoreboard():
    global scoreText, player_name, e
    player_name = canvas.create_text(570, 10, fill="white", font="Terminal 20 bold", text=e.get(), anchor="ne")
    scoreText = canvas.create_text(570, 40, fill="white", font="Terminal 30 bold", text=txt, anchor="ne")

def leaderboard():
    canvas.delete(ALL)
    canvas.create_image(0,0, image=leaderboard_background, anchor = "nw")
    columns= ("Name", "Score")
    my_Tree = ttk.Treeview(window, columns=columns, show='headings')
    my_Tree.column("Name", anchor=W, width=200)
    my_Tree.column("Score", anchor=W, width=120)
    my_Tree.heading("Name", text="Name", anchor=W)
    my_Tree.heading("Score", text="Score", anchor=W)
    sheet = []
    with open("highest_score_list.txt", "r") as score:
        for line in score:
            stripped_line = line.strip().split()
            sheet.append(stripped_line)
    count = 0
    for i in sheet:
        if i != " ":
            my_Tree.insert('', index='end', iid=count,values=(i[0], i[1]))
            count += 1
    canvas.create_window(300, 300, window=my_Tree)
    returnbutton = Button(canvas,image=leaderboard_return,command=mainmenu, borderwidth=0, background="#30b677")
    canvas.create_window(300,480, window=returnbutton)

def restart():
    global snake, run, score
    canvas.delete(ALL)
    Scoreboard()
    score = 0
    canvas.itemconfigure(scoreText, text=txt)
    snake = []
    create_snake()
    create_snake()
    create_snake()
    placeFood()
    run = True
    moveSnake()

def pause(_):
    global run, pause_text, P, Q, M, positions
    if run == False:
        run = True
        canvas.delete(P, pause_text, Q, M)
        canvas.after(speed,moveSnake)
    else:
        run = False
        pause_text = canvas.create_image(0,0, image=paused_menu, anchor = "nw")
        restartButton = Button(canvas,image=paused_menu_closed, borderwidth=0,background="#86cebb", command=restart)
        P = canvas.create_window(210,270, window=restartButton, anchor = "nw")
        quitButton = Button(canvas,image=paused_menu_exit, borderwidth=0,background="#71c8ab", command=window.destroy)
        Q = canvas.create_window(210, 330, window=quitButton, anchor = "nw")
        mainmenuButton = Button(canvas,image=paused_menu_main, borderwidth=0,background="#b7dce2", command=mainmenu)
        M = canvas.create_window(210, 210, window=mainmenuButton, anchor = "nw")
        print(positions)

def start():  
    global run, snake, score
    canvas.bind('<Escape>', pause)
    canvas.delete(ALL)
    canvas.bind("<Left>", leftKey)
    canvas.bind("<Right>", rightKey)
    canvas.bind("<Up>", upKey)
    canvas.bind("<Down>", downKey)
    canvas.focus_set()
    run = True
    Scoreboard()
    score = 0
    canvas.itemconfigure(scoreText, text=txt)
    snake = []
    create_snake()
    create_snake()
    create_snake()
    placeFood()
    moveSnake()

def playerName():
    global e
    canvas.delete(ALL)
    canvas.create_image(0,0, image=background, anchor = "nw")
    canvas.create_text(300,260,font='Terminal 20 bold', text="Player name:", fill='white' )
    e = Entry(canvas, width=40)
    canvas.create_window(300, 300, height=20, window = e)
    startButton = Button(canvas, image=playername_play, command=check, borderwidth=0, background="#5ebd8b")
    canvas.create_window(255, 325, window=startButton, anchor="nw")
    returnButton = Button(canvas, image=playername_return, command=mainmenu, borderwidth=0, background="#5ebd8b")
    canvas.create_window(255, 360, window=returnButton, anchor="nw")

def check():
    if e.get() == "":
        messagebox.showwarning(title=None, message="Enter name first")
    else:
        start()

def mainmenu():
    canvas.delete(ALL)
    canvas.create_image(0,0, image=background, anchor = "nw")
    startButton = Button(canvas, image=startmenu, command=playerName, borderwidth=0, background="#6dc195")
    canvas.create_window(210, 260, window=startButton,  anchor = "nw")
    leaderboardButton = Button(canvas, image=leaderboardmenu, command = leaderboard,  borderwidth=0, background="#59bc88")
    canvas.create_window(185, 330, window=leaderboardButton,  anchor = "nw")
    EXITButton = Button(canvas, image=quitmenu, command=window.destroy,  borderwidth=0, background="#40b97e")
    canvas.create_window(210, 400, window=EXITButton,  anchor = "nw")

width = 600 #canvas size
height = 600

window = Tk()
setWindowDimensions(width,height)

canvas = Canvas(window, bg="#6ac092", width=width, height=height)
canvas.pack()

#add images
background = PhotoImage(file="UI/Background.png")
startmenu = PhotoImage(file="UI/Background_start.png")
leaderboardmenu = PhotoImage(file="UI/Background_leaderboard.png")
quitmenu = PhotoImage(file="UI/Background_quit.png")
food_pic = PhotoImage(file="UI/apple.png")
paused_menu = PhotoImage(file="UI/Paused menu.png")
paused_menu_closed = PhotoImage(file="UI/Paused menu play.png")
paused_menu_exit = PhotoImage(file="UI/Paused menu quit.png")
paused_menu_main = PhotoImage(file="UI/Paused menu mainmenu.png")
playername_play = PhotoImage(file="UI/play.png")
playername_return = PhotoImage(file="UI/return.png")
gameover_restart = PhotoImage(file="UI/restart.png")
gameover_home = PhotoImage(file="UI/home.png")
gameover_exit = PhotoImage(file="UI/exit.png")
leaderboard_background = PhotoImage(file="UI/Leaderboard.png")
leaderboard_return = PhotoImage(file="UI/mainmenu.png")

snake = []
snakeSize = 20
score = 0
speed = 85
txt = str(score)

direction = "right"
run = True
pause_text = ""
P = ""
Q = ""
M = ""

mainmenu()

window.mainloop()