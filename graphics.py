import json
from pygments import lex
from pygments.lexers import PythonLexer
from tkinter import *
from tkinter import ttk

def all_themes():
	f=open('themes.json')
	file=json.load(f)
	f.close()
	themes=[]
	for i in file:
		themes.append(i)
	return themes

def read_themes(theme_name:str):
	f=open('themes.json')
	file=json.load(f)
	f.close()
	for i in file:
		if i == theme_name:
			# return(file[i])
			main=file[i][0]
			syntax=file[i][1]
			return main,syntax

def apply_theme(theme,text_widget):
	text_widget.config(background=theme["background"],
					foreground=theme["foreground"],
					selectbackground=theme["selectbackground"],
					insertbackground=theme["insertbackground"])
	

def enable_syntax(main_window,text_widget,syntax):
	for i in syntax:
		text_widget.tag_configure(i,foreground=syntax[i])
	def trig(e=None):
		trigger(text_widget)
	binding=main_window.bind('<Key>',trig)
	trigger(text_widget)
	return binding

def disable_syntax(main_window,text_widget,binding):
	main_window.unbind('<Key>',binding)
	for tag in text_widget.tag_names():
		if tag != 'sel':
			text_widget.tag_remove(tag,"1.0","end")

def trigger(textPad):
	textPad.mark_set("range_start", "1.0")
	data = textPad.get("1.0", "end")
	for tag in textPad.tag_names():
		if tag != 'sel':
			textPad.tag_remove(tag,"1.0","end")
	for token, content in lex(data, PythonLexer()):
		textPad.mark_set("range_end", "range_start + %dc" % len(content))
		textPad.tag_add(str(token), "range_start", "range_end")
		textPad.mark_set("range_start", "range_end")

# def start(main_window,text_widget):
# 	textPad=text_widget
# 	a,b=read_themes('dark_theme')
# 	apply_theme(a,b,textPad)
# 	main_window.bind('<Key>',trigger)
# 	trigger()

if __name__ == '__main__':
	syntax_enabled=False
	def enable(e=None):
		global bindvar
		bindvar=enable_syntax(root,text,syntax)
		syntax_enabled=True
	def disable(e=None):
		if syntax_enabled:
			global bindvar
			disable_syntax(root,text,bindvar)
			syntax_enabled=False
	def theadd(themename):
		print(themename)
		bkgrnd,synt=read_themes(themename)
		print(bkgrnd)
		apply_theme(bkgrnd,text)
	root=Tk()
	text=Text(root, height=30, width=100,font=('Consolas',13),wrap='none')
	text.pack(expand='yes',fill=BOTH)
	# theme,syntax=read_themes("dark_theme")
	# apply_theme(theme,text)
	theme_names=all_themes()
	menu=Menu(root)
	root.config(menu=menu)
	test=Menu(root,tearoff=0)
	menu.add_cascade(label='test',menu=test)
	test.add_command(label='start',command=enable)
	test.add_command(label='start',command=enable)
	themes=Menu(root,tearoff=0)
	menu.add_cascade(label='theme',menu=themes)
	for i in theme_names:
		themes.add_command(label=i,command=lambda : theadd(i))
	root.mainloop()
	# print(all_themes())