import tkinter as tk
import os
import random

from PIL import Image, ImageTk

number_of_constellations = 64
available_num = [x+1 for x in range(number_of_constellations)]
const_num = 0
const_name = ""

def constellation_picker():
    global const_num
    global const_name
    global available_num
    
    const_num = random.choice(available_num)
    available_num.remove(const_num)
    if len(available_num)==0:
        available_num = [x+1 for x in range(number_of_constellations)]

    selected_path = ""
    for f in os.listdir("photos\\"):
        if f.startswith(f"{str(const_num)}-"):
            selected_path = f"photos\\{f}"
            const_name = f.removeprefix(f"{const_num}-").removesuffix(".png")
    
    #rotate image randomly
    rotations = [0, 90, 180, 270]
    pic = Image.open(selected_path)
    pic = pic.rotate(random.choice(rotations))

    tk_pic = ImageTk.PhotoImage(pic)
    
    canvas.image = tk_pic
    canvas.create_image(0,0, image=tk_pic, anchor='nw')
    canvas.place(x=150,y=10)
    
def sumbit(events):
    if inp.get().strip().lower() == const_name:
        get_info()
        flicker(correct=True)
    else:
        flicker(correct=False)

    inp.delete(0, tk.END)

flick_count = 0      
def flicker(correct):
    global flick_count
    
    if flick_count%2==0:
        if correct:
            inp.configure(bg='green')
        else:
            inp.configure(bg='red')
    elif flick_count%2!=0:
        inp.configure(bg='white')

    flick_count+=1

    if flick_count<4:
        window.after(200, flicker, correct)
    else:
        flick_count=0

def get_info():
    target = ''
    name = ''
    obj = ''
    extra = ''
    with open("info.txt", 'r', encoding='utf-8') as f:
        txt = f.readlines()
        start, end = 0, 0
        for index, line in enumerate(txt):
            if line.startswith(f"{const_num}-"):
                start = index
            if line.startswith(f"{const_num+1}-") or index == len(txt)-1:
                end = index
                break
        target = txt[start:end]

    for line in target:
        if line.startswith("english:"):
            name += line
        elif line.startswith("greek:"):
            name += line.strip()
        elif line.startswith("*messier:"):
            obj += line
        elif line.startswith("*stars:"):
            obj += line.strip()
        
        if line.startswith("extra:"):
            extra += line.strip()

    
    i_name.configure(text=name)
    i_name.place(x=175,y=50)

    i_obj.configure(text=obj)
    i_obj.place(x=175,y=525)
    
    i_extra.configure(text=extra)
    i_extra.place(x=600,y=30)
    
    check_button.configure(command=next, text="next")
        
def next():
    global number_count
    #move away info
    i_name.place(x=-500, y=-500)
    i_obj.place(x=-500, y=-500)
    i_extra.place(x=-500, y=-500)

    number_count+=1
    if number_count>=number_of_constellations:
        i_number_count.configure(fg='green')
    i_number_count.configure(text=number_count)
    constellation_picker()
    check_button.configure(command=get_info, text="show")
    
        
#colors
bg_window = "#21212e"
bg_info = "#101017"

window = tk.Tk()
window.title("constellations")
window.geometry("900x700")
window.resizable(False, False)
window.configure(bg=bg_window)

icon = tk.PhotoImage(file="photos\\icon.png")
window.iconphoto(True, icon)

canvas = tk.Canvas(window, width=600, height=600)
constellation_picker()
                
inp = tk.Entry(font=("Rockwell", 18, 'bold'), justify="center")
inp.bind("<Return>", sumbit)
inp.place(x=320, y=625)

check_button = tk.Button(text="show",
                        font=("Rockwell", 12, 'bold'),
                        command=get_info, 
                        relief="raised", 
                        bd=3)
check_button.place(x=675, y=557) #y=577



#info
i_name = tk.Label(font=("Rockwell", 15, 'bold'),
                background=bg_window,
                justify="left",
                bg=bg_info,
                fg='white')

number_count=0
i_number_count = tk.Label(font=("Rockwell", 20, 'bold'), 
                text=number_count,
                background=bg_window,
                justify="left",
                fg='white')
i_number_count.place(x=600, y=622)

i_obj = tk.Label(font=("Rockwell", 15, 'bold'),
                background=bg_window,
                justify="left",
                bg=bg_info,
                fg='white')

i_extra = tk.Label(font=("Rockwell", 10, 'bold'),
                background=bg_window,
                justify="left",
                bg=bg_info,
                fg='white',
                wraplength=130)

incorrect = tk.Label(text="X", 
                     font=("Rockwell", 25, 'bold'),
                     fg='red',
                     bg=bg_window)


window.mainloop()