from tkinter import *
from random import randint
from winsound import Beep
from tkinter import ttk


# ============================ ФУНКЦИИ И МЕТОДЫ ==============================
# Останавливаем таймер
def stopTime():
    global timeRun, second

    if timeRun is not None:
        root.after_cancel(timeRun)

        # Убираем маркер работы таймера
        timeRun = None

    second = -1
    textTime['text'] = 'Время игры: 00 сек.'


# Возвращаем строку в виде ММ:СС
def getMinSec(s):
    # Находим минуты
    intMin = s // 60
    # Находим секунды
    intSec = s % 60
    textSecond = str(intSec)

    # Сбрасываем минуты, если прошло больше 59 (чтобы не вводить часы)
    if intMin > 59:
        intMin %= 60

    # Добавляем лидирующий ноль, если секунд меньше 10
    if intSec < 10:
        textSecond = '0' + textSecond

    if intMin == 0:
        return f'{textSecond} сек.'
    else:
        textMin = str(intMin)
        if intMin < 10:
            textMin = '0' + textMin
        return f'{textMin} мин. {textSecond} сек.'


# Обновляем текстовую метку таймера
def updateTime():
    global textTime, second, timeRun

    second += 1
    txt = f'Время игры: {getMinSec(second)}'
    textTime['text'] = txt
    root.update()
    timeRun = root.after(1000, updateTime)


# Перезапуск раунда
def restartRound():
    global sharik_go, green_pl, evilBot, go, vectorY_pl, \
        vectorY_bot, vectorY_sh, vectorX_sh, textBotCount, textPlcCunt

    cnv.delete(ALL)

    cnv.create_image(WIDTH // 2, (HEIGHT - 50) // 2, image=back)
    sharik_go = cnv.create_image(WIDTH // 2, HEIGHT // 2 - 25, image=sharik)
    green_pl = cnv.create_image(28, HEIGHT // 2 - 25, image=player0)
    evilBot = cnv.create_image(871, HEIGHT // 2 - 25, image=bot)
    cnv.create_text(390, 30, text='Игрок:', font='Arial 15')
    cnv.create_text(500, 30, text='Бот:', font='Arial 15')
    textBotCount = cnv.create_text(500, 60, text=f'{botCount}', font='Arial 14')
    textPlcCunt = cnv.create_text(390, 60, text=f'{playerCount}', font='Arial 14')

    vectorY_pl = None
    vectorY_sh = 0
    vectorX_sh = 0

    cnv.focus_set()


# Движение игрока
def movePlayer(vector):
    global vectorY_pl

    y = cnv.coords(green_pl)[1]

    if vector == UPKEY:
        if y > 70:
            vectorY_pl = -7
            cnv.move(green_pl, 0, vectorY_pl)
    elif vector == DOWNKEY:
        if y < 380:
            vectorY_pl = 7
            cnv.move(green_pl, 0, vectorY_pl)


# Движение шарика
def moveShar():
    global vectorY_bot, vectorY_sh, vectorX_sh, go, botCount, playerCount

    # Двигаем шарик
    if vectorY_sh != 0:
        cnv.move(sharik_go, vectorX_sh, vectorY_sh)
    # Если игра только началась, выбераем рандомное направление движ. шарика
    else:
        if randint(0, 1) == 0:
            vectorX_sh = 10
        else:
            vectorX_sh = -10

        if randint(0, 1) == 0:
            vectorY_sh = 10
        else:
            vectorY_sh = -10

    # Получаем координаты шарика
    x = cnv.coords(sharik_go)[0]
    y = cnv.coords(sharik_go)[1]

    # Проверяем шарик на столкновение с верхом и низом экрана
    if y > HEIGHT - 60 or y < 10:
        vectorY_sh = -vectorY_sh

    if x < 450:
        # Проверяем на победу бота
        if x < 10:
            botCount += 1
            Beep(500, 100)
            restartRound()
        # Проверяем шарик на столкновение с панелькой
        # Игрока
        if (x - 10) == 40:
            yPlayer = cnv.coords(green_pl)[1]
            if (yPlayer - 62) < y < (yPlayer + 62):
                vectorX_sh = -vectorX_sh
        # Симулируем жизнь бота*
        fake_move_bot()

    if x > 450:
        # Проверяем на победу игрока
        if x > WIDTH - 10:
            playerCount += 1
            Beep(500, 100)
            restartRound()
        # Проверяем шарик на столкновение с панелькой
        # Бота
        if (x + 10) == 860:
            yBot = cnv.coords(evilBot)[1]
            if (yBot - 62) < y < (yBot + 62):
                vectorX_sh = -vectorX_sh
        # Вызываем движение бота
        moveBot(y)

    go = root.after(17, moveShar)


# Симуляция живого соперника*
def fake_move_bot():
    global vectorY_bot

    y_bot = cnv.coords(evilBot)[1]

    if vectorY_bot is None:
        vectorY_bot = 2
    else:
        if vectorY_bot > 0:
            if 380 < y_bot:
                if speed_bot == 8:
                    vectorY_bot = -1
                else:
                    vectorY_bot = -4
        if vectorY_bot < 0:
            if y_bot < 70:
                if speed_bot == 8:
                    vectorY_bot = 1
                else:
                    vectorY_bot = 4

    cnv.move(evilBot, 0, vectorY_bot)


# Движение бота
def moveBot(y_sh):
    global vectorY_bot

    y_bot = cnv.coords(evilBot)[1]

    if y_sh < y_bot:
        if 70 < y_bot:
            vectorY_bot = -speed_bot
            cnv.move(evilBot, 0, vectorY_bot)
    elif y_sh > y_bot:
        if y_bot < 380:
            vectorY_bot = speed_bot
            cnv.move(evilBot, 0, vectorY_bot)


# Конец игры
def endRound():
    global vectorY_pl, vectorY_bot, vectorY_sh, \
        vectorX_sh, go, playerCount, botCount, speed_bot

    root.after_cancel(go)
    go = None

    startButton['state'] = NORMAL
    diffCombobox['state'] = NORMAL
    diffCombobox['state'] = 'readonly'
    resetButton['state'] = DISABLED
    playerCount = 0
    botCount = 0
    vectorY_bot = None
    speed_bot = 0

    diffCombobox.current(0)

    stopTime()
    restartRound()

    Beep(1200, 120)


# Начало игры
def startNewRound():
    global speed_bot

    Beep(900, 120)

    startButton['state'] = DISABLED
    diffCombobox['state'] = DISABLED
    resetButton['state'] = NORMAL

    if diffCombobox.current() == 0:
        speed_bot = 6
    elif diffCombobox.current() == 1:
        speed_bot = 7
    elif diffCombobox.current() == 2:
        speed_bot = 8

    cnv.focus_set()

    updateTime()
    moveShar()


# ============================ НАЧАЛО ПРОГРАММЫ ==============================
# Размеры окна
WIDTH = 900
HEIGHT = 500

# Очки игрока
playerCount = 0
# Очки противника
botCount = 0

root = Tk()
root.resizable(False, False)
root.title('Самодельный тенис v.1.0')
root.iconbitmap('icon.ico')
root.configure(bg='gray')

POS_X = root.winfo_screenwidth() // 2 - WIDTH // 2
POS_Y = root.winfo_screenheight() // 2 - HEIGHT // 2
root.geometry(f'{WIDTH}x{HEIGHT}+{POS_X}+{POS_Y}')

cnv = Canvas(root, width=WIDTH, height=(HEIGHT - 50))
cnv.config(highlightthickness=0)
cnv.place(x=0, y=50)
cnv.focus_set()

# Изображение игрового поля
back = PhotoImage(file='pole.png')
cnv.create_image(WIDTH // 2, (HEIGHT - 50) // 2, image=back)

# Счёт текущей игры
cnv.create_text(390, 30, text='Игрок:', font='Arial 15')
cnv.create_text(500, 30, text='Бот:', font='Arial 15')
textBotCount = cnv.create_text(500, 60, text=f'{botCount}', font='Arial 14')
textPlcCunt = cnv.create_text(390, 60, text=f'{playerCount}', font='Arial 14')

# Названия степеней сложности
itemDiff = ['Легко)', 'Нормально...', 'Сложно!']

# Впадающий список
diffCombobox = ttk.Combobox(root, width=20, values=itemDiff, state='readonly')
diffCombobox.place(x=750, y=15)
diffCombobox.current(0)

# Изображение шарика
sharik = PhotoImage(file='shar.png')
sharik_go = cnv.create_image(WIDTH // 2, HEIGHT // 2 - 25, image=sharik)

# Изображение игрока
player0 = PhotoImage(file='player.png')
green_pl = cnv.create_image(28, HEIGHT // 2 - 25, image=player0)

# Изображение противника
bot = PhotoImage(file='evilBot.png')
evilBot = cnv.create_image(871, HEIGHT // 2 - 25, image=bot)

# Кнопка: начать игру
startButton = Button(root, text='НАЧАТЬ ИГРУ', width=15, height=2, font='Arial 10', bg='gray', fg='yellow')
startButton.place(x=2, y=3)
startButton['command'] = startNewRound

# Кнопка: закончить игру
resetButton = Button(root, text='ЗАКОНЧИТЬ ИГРУ', width=15, height=2, font='Arial 10', bg='gray', fg='yellow')
resetButton.place(x=140, y=3)
resetButton['command'] = endRound
resetButton['state'] = DISABLED

# Метка сложности
Label(root, bg='gray', fg='yellow', text='Выбор сложности:', font='Arial 15').place(x=570, y=10)

# Текстовая строка, показывающая время
textTime = Label(text='Время игры: 00 сек.', font='Arial 15', bg='gray', fg='white')
textTime.place(x=300, y=10)
# Прошедшее время
second = -1

# Переменная для таймера
# Необходима, чтобы останавливать работу root.after()
timeRun = None

# Константы-коды для направления движения
UPKEY = 0
DOWNKEY = 1

# Скорость и направление движения
# Игрока
vectorY_pl = None
# Бота
vectorY_bot = None
speed_bot = 0
# Шарика
vectorY_sh = 0
vectorX_sh = 0

# Назначаем клавиши управления курсором
cnv.bind('<Up>', lambda e, x=UPKEY: movePlayer(x))
cnv.bind('<Down>', lambda e, x=DOWNKEY: movePlayer(x))

# Переменная для работы root.after(17, moveShar)
go = None

root.mainloop()
