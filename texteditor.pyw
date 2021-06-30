#!/usr/bin/python3
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
import subprocess
import platform
import graphics

global open_status_name,curtheme,syntax,syntax_enabled,bindvar
syntax_enabled=False
open_status_name = False

def checkos():
	operating_system=(str(platform.node())).lower()
	return operating_system

def test_code(interactive_mode:bool):
	if text.tag_ranges("sel"):
		first=text.index(SEL_FIRST)
		first=first+" linestart"
		last=text.index(SEL_LAST)
		last=last+" lineend"
	else:
		curpos=text.index(INSERT)
		first=curpos+" linestart"
		last=curpos+" lineend"

	code=text.get(first,last)
	open("testing-code.py", 'w').write(code) 
	os=checkos()
	if os=='sunday':
		if interactive_mode:
			command="start cmd /c \" python -i testing-code.py \""
		else:
			command = "start cmd /c \" python testing-code.py && echo. && pause || echo. && pause \""
	elif os=='kali':
		if interactive_mode:
			command='xfce4-terminal -e "python -i testing-code.py"'
		else:
			command='xfce4-terminal --hold -e "python testing-code.py"'
	subprocess.run(command,shell=True) 

def comment(e):
	if text.tag_ranges("sel"):
		first=text.index(SEL_FIRST)
		first=int(float(first))
		last=text.index(SEL_LAST)
		last=int(float(last))
	else:
		curpos=text.index(INSERT)
		first=int(float(curpos))
		last=int(float(curpos))
	is_commented=True
	for i in range(first,last+1):
		pos1=str(i)+".0"
		pos2=str(i)+".1"
		a=text.get(pos1,pos2)
		if a!='#':
			is_commented=False
	if is_commented:
		for i in range(first,last+1):
			pos1=str(i)+".0"
			pos2=str(i)+".1"
			text.delete(pos1,pos2)
	else:
		for i in range(first,last+1):
			pos=str(i)+".0"
			text.insert(pos,"#")
	return 'break'

def run(interactive:bool):
	save(False)
	global open_status_name
	if open_status_name:
		os=checkos()
		if os=="sunday":
			if interactive:
				command="start cmd /c \" python -i \""+open_status_name+"\" \""
			else:
				command="start cmd /c \" python \""+open_status_name+"\" && echo. && pause || echo. && pause \""
		elif os=='kali':
			if interactive:
				command='xfce4-terminal -e "python -i '+open_status_name+'"'
			else:
				command='xfce4-terminal --hold -e "python '+open_status_name+'"'
		subprocess.run(command,shell=True)

def tab(e=None):
    text.insert(INSERT, "    ")
    return 'break'

def enter(e=None):
	currentline = text.get(text.index(INSERT)+' linestart',INSERT)
	# currentcode = currentline.split("#")[0].rstrip()
	currentcode = currentline.split("#")[0]
	toinsert='\n'
	try:
		if currentcode.rstrip()[-1]==':':
			toinsert+="    "
	except IndexError:
		pass
	current_leading_spaces=len(currentcode)-len(currentcode.lstrip())
	toinsert+=" "*current_leading_spaces
	text.insert(INSERT,toinsert)
	return 'break'

def duplicate(e=None):
	cursorpos = text.index(INSERT)
	line = "\n"+text.get(cursorpos+' linestart',cursorpos+' lineend')
	text.insert(cursorpos+" lineend",line)
	return 'break'

def text_right_click(event):
	try:
		modmenu.tk_popup(event.x_root, event.y_root)
	finally:
		modmenu.grab_release()


def kill():
    if messagebox.askokcancel("Quit", "Do you want to quit?\n(any unsaved data will be lost!)",icon="warning"):
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
		if syntax_enabled:
			rem_syntax()
			add_syntax()

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
		if syntax_enabled:
			rem_syntax()
			add_syntax()

def change_theme(theme_name):
	global curtheme,syntax,syntax_enabled
	curtheme=theme_name
	bgrnd,syntax=graphics.read_themes(theme_name)
	graphics.apply_theme(bgrnd,text)
	if syntax_enabled:
		rem_syntax()
		add_syntax()

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
		pass

def clear():
	sel = text.get(SEL_FIRST, SEL_LAST)
	text.delete(SEL_FIRST, SEL_LAST)

def clearall():
	text.delete(1.0 , END)

def add_syntax():
	global syntax_enabled,syntax,bindvar
	mysyn=syntax
	bindvar=graphics.enable_syntax(root,text,mysyn)
	syntax_enabled=True
	pass

def rem_syntax():
	global syntax_enabled
	if syntax_enabled:
		global bindvar
		bindingvar=bindvar
		graphics.disable_syntax(root,text,bindingvar)
		syntax_enabled=False
	pass

root = Tk()
root.title("Test pad")
# root.iconbitmap("ide.ico")
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
modmenu.add_separator()
modmenu.add_command(label="Comment", command=lambda: comment(False))
modmenu.add_separator()
modmenu.add_command(label = "Clear", command = clear)
modmenu.add_command(label = "Clear all", command = clearall)
modmenu.add_separator()
modmenu.add_command(label="Run", command=lambda: run(False))
modmenu.add_command(label="Run interactive", command=lambda: run(True))
modmenu.add_separator()
modmenu.add_command(label="Test Code", command=lambda: test_code(False))
modmenu.add_command(label="Test interactive", command=lambda: test_code(True))

formatmenu = Menu(menu,tearoff=0)
menu.add_cascade(label="Format",menu = formatmenu)
# formatmenu.add_command(label="Dark Theme",command=dark_theme)
# formatmenu.add_command(label="Light Theme",command=light_theme)
theme_names=graphics.all_themes()
for i in theme_names:
	formatmenu.add_command(label=i,command= lambda i=i: change_theme(i))
formatmenu.add_separator()
formatmenu.add_command(label="syntax Highlighting",command=add_syntax)
formatmenu.add_command(label="No syntax Highlighting",command=rem_syntax)

execmenu = Menu(menu,tearoff=0)
menu.add_cascade(label="Run",menu=execmenu)
execmenu.add_command(label="Run",command=lambda: run(False))
execmenu.add_command(label="Run interactive",command=lambda: run(True))
execmenu.add_separator()
execmenu.add_command(label="Test Code",command=lambda: test_code(False))
execmenu.add_command(label="Test interactive",command=lambda: test_code(True))

# text = Text(root, height=30, width=60, font = ("Hurmit NF", 10),undo=True)
# text = Text(root, height=30, width=60, font = ("Consolas", 13),undo=True,padx=10,pady=10,wrap='none')
text = Text(root, height=30, width=60, font = ("Consolas", 13),undo=True,wrap='none')
change_theme(theme_names[0])
add_syntax()
# dark_theme()
# add_syntax()
scrolly = Scrollbar(root, command=text.yview)
scrollx = Scrollbar(root, command=text.xview, orient=HORIZONTAL)                 
text.config(yscrollcommand=scrolly.set)
text.config(xscrollcommand=scrollx.set)           
scrolly.pack(side=RIGHT, fill=Y)
scrollx.pack(side=BOTTOM, fill=X)
text.pack(side=LEFT, expand=True, fill=BOTH)
text.bind("<Button-3>", text_right_click)
text.bind('<Control-slash>',comment)
text.bind("<Tab>", tab)
text.bind("<Return>", enter)
text.bind("<Control-d>", duplicate)

root.protocol("WM_DELETE_WINDOW", kill)
root.mainloop()
