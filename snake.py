from tkinter import Tk, Canvas
import random

# размеры окна
WIDTH = 800
HEIGHT = 600
# размер блока змеи
BLOCK_SIZE = 20
# состояние игры
IN_GAME = True



def create_block():
    #создание блоков на игровом поле
    global BLOCK
    posx = BLOCK_SIZE * random.randint(1, (WIDTH-BLOCK_SIZE) / BLOCK_SIZE)
    posy = BLOCK_SIZE * random.randint(1, (HEIGHT-BLOCK_SIZE) / BLOCK_SIZE)
    BLOCK = c.create_oval(posx, posy, posx+BLOCK_SIZE, posy+BLOCK_SIZE, fill="blue")


def main():
    global IN_GAME
    if IN_GAME:
        s.move()
        # положение первого блока
        first_block = c.coords(s.blocks[-1].instance)
        x1, y1, x2, y2 = first_block
        # если сталкивается с краями игрового поля
        if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
            IN_GAME = False
        # съедает блок
        elif first_block == c.coords(BLOCK):
            s.add_block()
            c.delete(BLOCK)
            create_block()
        # если сталкивается сама с собой
        else:
            for index in range(len(s.blocks)-1):
                if first_block == c.coords(s.blocks[index].instance):
                    IN_GAME = False
        root.after(100, main)
    # если IN_GAME = false останавливаем игру
    else:
        set_state(restart_text, 'normal')
        set_state(game_over_text, 'normal')


class Block(object):
    # класс блока змеи
    def __init__(self, x, y):
        self.instance = c.create_rectangle(x, y, x+BLOCK_SIZE, y+BLOCK_SIZE, fill="white")


class Snake(object):
    def __init__(self, blocks):
        self.blocks = blocks
        # возможные направления движения
        self.mapping = {"Down": (0, 1), "Right": (1, 0),
                        "Up": (0, -1), "Left": (-1, 0)}
        # стартовое направление движения
        self.vector = self.mapping["Right"]

    def move(self):
        # функция движения змеи
        # проходим циклом по всем блокам кроме первого
        for index in range(len(self.blocks)-1):
            block = self.blocks[index].instance
            x1, y1, x2, y2 = c.coords(self.blocks[index+1].instance)
            c.coords(block, x1, y1, x2, y2)
        # координаты блока перед первым
        x1, y1, x2, y2 = c.coords(self.blocks[-2].instance)
        # сдвигаем первый блок
        c.coords(self.blocks[-1].instance,
                 x1+self.vector[0]*BLOCK_SIZE, y1+self.vector[1]*BLOCK_SIZE,
                 x2+self.vector[0]*BLOCK_SIZE, y2+self.vector[1]*BLOCK_SIZE)

    def add_block(self):
        # добавляем новый блок
        last_seg = c.coords(self.blocks[0].instance)
        x = last_seg[2] - BLOCK_SIZE
        y = last_seg[3] - BLOCK_SIZE
        self.blocks.insert(0, Block(x, y))

    def change_direction(self, event):
        # изменение направления движения
        # event передает символ нажатой клавиши
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]

    def reset_snake(self):
        for block in self.blocks:
            c.delete(block.instance)


def set_state(item, state):
    c.itemconfigure(item, state=state)


def clicked(event):
    global IN_GAME
    s.reset_snake()
    IN_GAME = True
    c.delete(BLOCK)
    c.itemconfigure(restart_text, state='hidden')
    c.itemconfigure(game_over_text, state='hidden')
    start_game()


def start_game():
    global s
    create_block()
    s = create_snake()
    # Reaction on keypress
    c.bind("<KeyPress>", s.change_direction)
    main()


def create_snake():
    # создаем три блока змеи
    blocks = [Block(BLOCK_SIZE, BLOCK_SIZE),
                Block(BLOCK_SIZE*2, BLOCK_SIZE),
                Block(BLOCK_SIZE*3, BLOCK_SIZE)]
    return Snake(blocks)


root = Tk()# экз класса Tk, главное окно
root.title("Snake on Python") # заголовок окна

c = Canvas(root, width=WIDTH, height=HEIGHT, bg="gray") #экземляр класса canvas
c.grid()
c.focus_set() # объект с в фокусе чтобы ловить нажатие клавиш
game_over_text = c.create_text(WIDTH/2, HEIGHT/2, text="GAME OVER!", font='Arial 20', fill='red', state='hidden')
restart_text = c.create_text(WIDTH/2, HEIGHT-HEIGHT/3,
                             font='Arial 30',
                             fill='white',
                             text="Начать заново",
                             state='hidden')
c.tag_bind(restart_text, "<Button-1>", clicked)
start_game()
root.mainloop()