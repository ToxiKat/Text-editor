from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import colorchooser
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename, asksaveasfilename
import subprocess

global open_status_name
open_status_name = False

def test_code():
    code=text.selection_get()
    open("testing-code.py", 'w').write(code) 
    command = "start cmd /c \" python testing-code.py && echo. && pause || echo. && pause \""
    subprocess.run(command,shell=True)
    open("testing-code.py", 'w').write("") 

def run():
    save(False)
    global open_status_name
    if open_status_name:
        command="start cmd /c \" python \""+open_status_name+"\" && echo. && pause || echo. && pause \""
        subprocess.run(command,shell=True)

def dark_theme():
    text.config(insertbackground="cyan")
    text.config(background='#2a2a2a')
    text.config(foreground='#ffffff')

def light_theme():
    text.config(insertbackground="black")
    text.config(background='#ffffff')
    text.config(foreground='#000000')

def text_right_click(event):
    try:
        modmenu.tk_popup(event.x_root, event.y_root)
    finally:
        modmenu.grab_release()

def font():
    (triple,color) = askcolor()
    if color:
       text.config(foreground=color)

def kill():
    root.destroy()

def new_file(e):
    global open_status_name
    open_status_name=False
    clearall()

def opn(e):
    text.delete(1.0 , END)
    filename=askopenfilename(title="Open Python File",filetypes=[('Python Files','*.py *.pyw')])
    file = open(filename , 'r')
    if file:
        txt = file.read()
        text.insert(INSERT,txt)
        global open_status_name
        open_status_name=filename

def save(e):
    global open_status_name
    if open_status_name:
        alltext = text.get(1.0,END)
        open(open_status_name,'w').write(alltext)
    else:
        saveas()

def saveas():
    filename = asksaveasfilename(title="Save As",defaultextension=".py",filetypes=[('Python Files','*.py *.pyw')])
    if filename:
        alltext = text.get(1.0, END)                      
        open(filename, 'w').write(alltext) 
        text.delete(1.0,END)
        file = open(filename, 'r')
        txt=file.read()
        text.insert(INSERT,txt)
        global open_status_name
        open_status_name=filename

def cut():
    copy()
    clear()

def copy():
    text.clipboard_clear()
    text.clipboard_append(text.selection_get()) 

def paste():
    try:
        teext = text.selection_get(selection='CLIPBOARD')
        text.insert(INSERT, teext)
    except:
        tkMessageBox.showerror("Error","The clipboard is empty!")

def clear():
    sel = text.get(SEL_FIRST, SEL_LAST)
    text.delete(SEL_FIRST, SEL_LAST)

def clearall():
    text.delete(1.0 , END)

def background():
    (triple,color) = askcolor()
    if color:
       text.config(background=color)

root = Tk()
root.title("Test pad")
root.iconbitmap("ide.ico")
menu = Menu(root)

filemenu = Menu(root,tearoff=0)
root.config(menu = menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New File", command=lambda: new_file(False))
root.bind('<Control-n>',new_file)
filemenu.add_command(label="Open", command=lambda: opn(False))
root.bind('<Control-o>',opn)
filemenu.add_command(label="Save", command=lambda: save(False))
root.bind('<Control-s>',save)
filemenu.add_command(label="Save as", command=saveas)
filemenu.add_separator()
filemenu.add_command(label="Close", command=kill)

modmenu = Menu(root,tearoff=0)
modmenu.add_command(label="cut",command=cut)
modmenu.add_command(label="Copy", command = copy)
modmenu.add_command(label="paste", command=paste)
modmenu.add_command(label = "Clear", command = clear)
modmenu.add_command(label = "Clear all", command = clearall)
modmenu.add_command(label="Run", command=run)
modmenu.add_command(label="Test Code", command=test_code)

formatmenu = Menu(menu,tearoff=0)
menu.add_cascade(label="Format",menu = formatmenu)
formatmenu.add_cascade(label="font", command = font)
formatmenu.add_command(label="background", command=background)
formatmenu.add_separator()
formatmenu.add_command(label="Dark Theme",command=dark_theme)
formatmenu.add_command(label="Light Theme",command=light_theme)

execmenu = Menu(menu,tearoff=0)
menu.add_cascade(label="Execute",menu=execmenu)
execmenu.add_command(label="Execute",command=run)
execmenu.add_command(label="Test Code",command=test_code)

# text = Text(root, height=30, width=60, font = ("Hurmit NF", 10),undo=True)
text = Text(root, height=30, width=60, font = ("Consolas", 10),undo=True)
dark_theme()

scroll = Scrollbar(root, command=text.yview)
scroll.config(command=text.yview)                  
text.config(yscrollcommand=scroll.set)           
scroll.pack(side=RIGHT, fill=Y)
text.pack(side=LEFT, expand=True, fill=BOTH)
text.bind("<Button-3>", text_right_click)

root.mainloop()