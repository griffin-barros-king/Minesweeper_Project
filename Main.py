from tkinter import *
from tkinter import messagebox

   
#current method of determining board
map = [
   [1, 0, 0, 0, 1, 0, 0, 0, 0],
   [0, 0, 0, 0, 0, 0, 0, 0, 0],
   [0, 0, 1, 1, 0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0, 1, 0, 0, 0],
   [0, 0, 0, 0, 0, 0, 0, 0, 0],
   [0, 0, 0, 1, 0, 1, 0, 0, 0],
   [0, 0, 0, 0, 0, 0, 1, 0, 0],
   [0, 0, 0, 1, 0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0, 0, 0, 0, 1]
]

top = Tk()
top.geometry("144x210")

class Buttton():
   
    def __init__(self, x, y, loc, ):
        self.label = ''
        self.opened = False
        self.x = x
        self.y = y
        self.loc = loc
        self.button = Button(top, text = ' ', height = 1, width = 1, bg = 'blue')
        self.first_click = True
        return

    
    def regen(self):
        fix_map(self.x, self.y)
        regenerate()
        top_buttons[(self.x, self.y)].left_click(None)
        for key in top_buttons.keys():
            top_buttons[key].first_click = False
        return
        
    
    def left_click(self, x):
        if self.button.cget('text') == 'F':
            return
        if bottom_buttons[(self.x, self.y)].val == 'B':
            if self.first_click:
                self.regen()
                return
            bottom_buttons[(self.x, self.y)].button.config(bg='red')
            for key in top_buttons.keys():
                top_buttons[key].button.destroy()
            msg=messagebox.showinfo("L", "YOU HIT A MINE:(")
            return
        if self.first_click:
            for key in top_buttons.keys():
                top_buttons[key].first_click = False
        if bottom_buttons[(self.x, self.y)].val == ' ':
            self.open_neighbors(False)
            self.opened = True
        self.button.destroy()
        if (self.x, self.y) in safe_top_buttons.keys():
            safe_top_buttons.pop((self.x, self.y))
        self.check_win()
        return
        

    def right_click(self, x):
        if self.button.cget('text') == ' ':
            self.button.config(text = 'F')
            self.label = 'F'
        else:
            self.button.config(text = ' ')
            self.label = ''
        return


    def place(self):
        self.button.bind('<ButtonRelease-1>', self.left_click)
        self.button.bind('<Button-2>', self.right_click)
        self.button.bind('<Button-3>', self.right_click)
        self.button.place(x = self.x * 16, y = self.y * 23)
        return


    def open(self, test):
        if bottom_buttons[test].val == ' ':
            top_buttons[test].open_neighbors(False)
            top_buttons[test].opened = True
            top_buttons[test].button.destroy()
            if ((top_buttons[test].x, top_buttons[test].y)) in safe_top_buttons.keys():
                safe_top_buttons.pop((top_buttons[test].x, top_buttons[test].y))
        elif bottom_buttons[test].val != 'B':
            top_buttons[test].opened = True
            top_buttons[test].button.destroy()
            if ((top_buttons[test].x, top_buttons[test].y)) in safe_top_buttons.keys():
                safe_top_buttons.pop((top_buttons[test].x, top_buttons[test].y))
        return


    def open_neighbors(self, chord):
        if self.opened:
            if not chord:
                return
        print(f'start {self.x} {self.y}')
        self.opened = True
        num = 0
        if self.x > 0:
            if self.y > 0:
                test = (self.x-1,self.y-1)
                self.open(test)
                
            if self.y < len(map) - 1:
                test = (self.x-1,self.y+1)
                self.open(test)
                    
            test = (self.x-1,self.y)
            self.open(test)
                
            if self.x < len(map[0]) - 1:
                if self.y > 0:
                    test = (self.x+1,self.y-1)
                    self.open(test)
                if self.y < len(map) - 1:
                    test = (self.x+1,self.y+1)
                    self.open(test)
                test = (self.x+1,self.y)
                self.open(test)
        elif self.x < len(map) - 1:
            if self.y > 0:
                test = (self.x+1,self.y-1)
                self.open(test)
            if self.y < len(map) - 1:
                test = (self.x+1,self.y+1)
                self.open(test) 
            test = (self.x+1,self.y)
            self.open(test)

        if self.y > 0:
            test = (self.x, self.y-1)
            self.open(test)
        if self.y < len(map[0]) - 1:
            test = (self.x, self.y+1)
            self.open(test)
        return
    

    def check_win(self):
        if len(safe_top_buttons) == 0:
            for key in top_buttons.keys():
                top_buttons[key].button.destroy()
            msg=messagebox.showinfo("W", "YOU WIN :D")
        return




class underButtton():
   
    def __init__(self, x, y, val, loc):
        self.val = val
        self.loc = loc
        self.x = x
        self.y = y
        self.button = Button(top, text = val, height = 1, width = 1)
        if self.val == 'B':
            self.button.config(bg = 'orange')
        return

    
    def left_click(self, x):
        self.chord()
        return


    def place(self):
        self.button.bind('<ButtonRelease-1>', self.left_click)
        self.button.place(x = self.x * 16, y = self.y * 23)
        return


    def chord(self):
        if self.val == ' ':
            return
    

        flags = 0
        if self.x > 0:
            if self.y > 0:
                if top_buttons[(self.x-1,self.y-1)].label == 'F':
                    flags += 1
            if self.y < len(map) - 1:
                if top_buttons[(self.x-1,self.y+1)].label == 'F':
                    flags += 1
            if top_buttons[(self.x-1,self.y)].label == 'F':
                flags += 1
            if self.x < len(map[0]) - 1:
                if self.y > 0:
                    if top_buttons[(self.x+1,self.y-1)].label == 'F':
                        flags += 1
                if self.y < len(map) - 1:
                    if top_buttons[(self.x+1,self.y+1)].label == 'F':
                        flags += 1
                if top_buttons[(self.x+1,self.y)].label == 'F':
                    flags += 1
        elif self.x < len(map[0]) - 1:
            if self.y > 0:
                if top_buttons[(self.x+1,self.y-1)].label == 'F':
                    flags += 1
            if self.y < len(map) - 1:
                if top_buttons[(self.x+1,self.y+1)].label == 'F':
                    flags += 1
            if top_buttons[(self.x+1,self.y)].label == 'F':
                flags += 1

        if self.y > 0:
            if top_buttons[(self.x,self.y-1)].label == 'F':
                flags += 1
        if self.y < len(map) - 1:
            if top_buttons[(self.x,self.y+1)].label == 'F':
                flags += 1

        if flags == int(self.val):
            top_buttons[(self.x, self.y)].open_neighbors(True)
        top_buttons[(0,0)].check_win()
        return




def get_neighbors(x, y):
    if map[y][x] == 1:
        return 'B'
    
    num = 0
    if y > 0:
        if x > 0:
            if map[y-1][x-1] == 1:
                num += 1
        if x < len(map[0]) - 1:
            if map[y-1][x+1] == 1:
                num += 1
        if map[y-1][x] == 1:
            num += 1
        if y < len(map) - 1:
            if x > 0:
                if map[y+1][x-1] == 1:
                    num += 1
            if x < len(map[0]) - 1:
                if map[y+1][x+1] == 1:
                    num += 1
            if map[y+1][x] == 1:
                num += 1
    elif y < len(map) - 1:
        if x > 0:
            if map[y+1][x-1] == 1:
                num += 1
        if x < len(map[0]) - 1:
            if map[y+1][x+1] == 1:
                num += 1
        if map[y+1][x] == 1:
            num += 1

    if x > 0:
        if num == 0:
            print('HELLO')
        if map[y][x-1] == 1:
            num += 1
            if x == 3 and y == 0:
                print('HI')
    if x < len(map[0]) - 1:
        if map[y][x+1] == 1:
            num += 1

    if num == 0:
        return ' '
    return f'{num}'


def fix_map(x, y):
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == 0:
                if x != j or y != i:
                    map[i][j] = 1
                    map[y][x] = 0
                    print(map)
                    print(i)
                    print(j)
                    return
    return
    

def regenerate():
    global top_buttons
    global bottom_buttons
    global safe_top_buttons
    loc = 0
    bottom_buttons = {}
    safe_top_buttons = {}
    for i in range(len(map)):
        for j in range(len(map[0])):
            n = get_neighbors(j, i)
            x = underButtton(j, i, n, loc)
            x.place()
            bottom_buttons[(j, i)] = x
            y = Buttton(j,i, loc)
            y.place()
            top_buttons[(j, i)] = y
            if n != 'B':
                safe_top_buttons[(j, i)] = y
            loc +=1
    return

#initial board generation
num_gens = 0
loc = 0
top_buttons = {}
bottom_buttons = {}
safe_top_buttons = {}
for i in range(len(map)):
    for j in range(len(map[0])):
        n = get_neighbors(j, i)
        x = underButtton(j, i, n, loc)
        x.place()
        bottom_buttons[(j, i)] = x
        y = Buttton(j,i, loc)
        y.place()
        top_buttons[(j, i)] = y
        if n != 'B':
            safe_top_buttons[(j, i)] = y
        loc +=1


top.mainloop()
      
