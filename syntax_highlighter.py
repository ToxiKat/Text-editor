import sys
import builtins
import re
import keyword
import tkinter

global is_started
is_started=False

def any(name, alternates):
	"Return a named group pattern matching list of alternates."
	return "(?P<%s>" % name + "|".join(alternates) + ")"

def ty():
	kw = r"\b" + any("KEYWORD", keyword.kwlist) + r"\b"
	builtinlist = [str(name) for name in dir(builtins)
										if not name.startswith('_')]
	# builtinlist.remove('print')
	builtin = r"([^.'\"\\#]\b|^)" + any("BUILTIN", builtinlist) + r"\b"
	comment = any("COMMENT", [r"#[^\n]*"])
	stringprefix = r"(\br|u|ur|R|U|UR|Ur|uR|b|B|br|Br|bR|BR)?"
	sqstring = stringprefix + r"'[^'\\\n]*(\\.[^'\\\n]*)*'?"
	dqstring = stringprefix + r'"[^"\\\n]*(\\.[^"\\\n]*)*"?'
	sq3string = stringprefix + r"'''[^'\\]*((\\.|'(?!''))[^'\\]*)*(''')?"
	dq3string = stringprefix + r'"""[^"\\]*((\\.|"(?!""))[^"\\]*)*(""")?'
	string = any("STRING", [sq3string, dq3string, sqstring, dqstring])
	return kw + "|" + builtin + "|" + comment + "|" + string +\
		   "|" + any("SYNC", [r"\n"])

def _coordinate(start,end,string):
	srow=string[:start].count('\n')+1 # starting row
	scolsplitlines=string[:start].split('\n')
	if len(scolsplitlines)!=0:
		scolsplitlines=scolsplitlines[len(scolsplitlines)-1]
	scol=len(scolsplitlines)# Ending Column
	lrow=string[:end+1].count('\n')+1
	lcolsplitlines=string[:end].split('\n')
	if len(lcolsplitlines)!=0:
		lcolsplitlines=lcolsplitlines[len(lcolsplitlines)-1]
	lcol=len(lcolsplitlines)+1# Ending Column
	return '{}.{}'.format(srow, scol),'{}.{}'.format(lrow, lcol)#, (lrow, lcol)

def coordinate(pattern, string,txt):
	line=string.splitlines()
	start=string.find(pattern)  # Here Pattern Word Start
	end=start+len(pattern) # Here Pattern word End
	srow=string[:start].count('\n')+1 # starting row
	scolsplitlines=string[:start].split('\n')
	if len(scolsplitlines)!=0:
		scolsplitlines=scolsplitlines[len(scolsplitlines)-1]
	scol=len(scolsplitlines)# Ending Column
	lrow=string[:end+1].count('\n')+1
	lcolsplitlines=string[:end].split('\n')
	if len(lcolsplitlines)!=0:
		lcolsplitlines=lcolsplitlines[len(lcolsplitlines)-1]
	lcol=len(lcolsplitlines)# Ending Column
	return '{}.{}'.format(srow, scol),'{}.{}'.format(lrow, lcol)#, (lrow, lcol)

def check(k={}):
	if k['COMMENT']!=None:
		return 'comment','red'
	elif k['BUILTIN']!=None:
		return 'builtin','VioletRed'
	elif k['STRING']!=None:
		return 'string','green'
	elif k['KEYWORD']!=None:
		return 'keyword','orange'
	else:
		return 'ss','NILL'

txtfilter=re.compile(ty(),re.S)

def start(txtbox=None):
	global txt
	txt=txtbox
	global bind1
	bind1=txt.bind("<Any-KeyPress>", trigger)
	global bind2
	bind2=txt.bind("<ButtonRelease-1>", trigger)
	global bind3
	bind3=txt.bind("<ButtonRelease-2>", trigger)
	global bind4
	bind4=txt.bind("<ButtonRelease-3>", trigger)
	global is_started
	is_started=True
	trigger(None)

def stop():
	global is_started
	if is_started:
		global txt,bind1,bind2,bind3,bind4
		for tag in txt.tag_names():
			txt.tag_remove(tag, "1.0", "end")

		txt.unbind("<Any-KeyPress>",bind1)
		txt.unbind("<ButtonRelease-1>",bind2)
		txt.unbind("<ButtonRelease-2>",bind3)
		txt.unbind("<ButtonRelease-3>",bind4)

# def binding_functions_configuration():
# 	txt.storeobj['ColorLight']=trigger
# 	return

def trigger(event=None):
	val=txt.get('1.0','end')
	if len(val)==1:
		return
	for i in ['comment','builtin','string','keyword']:
		txt.tag_remove(i,'1.0','end')
	for i in txtfilter.finditer(val):
		start=i.start()
		end=i.end()-1
		tagtype,color=check(k=i.groupdict())
		if color!='NILL':
			ind1,ind2=_coordinate(start,end,val)
			txt.tag_add(tagtype,ind1, ind2)
			txt.tag_config(tagtype,foreground=color)



if __name__ == '__main__':

	root=tkinter.Tk()
	menu=tkinter.Menu(root)
	txt=tkinter.Text(root)
	root.config(menu=menu)
	test=tkinter.Menu(menu,tearoff=0)
	menu.add_cascade(label="test",menu=test)
	test.add_command(label="start",command=lambda: start(txt))
	test.add_command(label="stop",command=stop)
	txt.pack(expand='yes')
	# txt.storeobj={}

	store=start(txtbox=txt)
	# tkinter.Button(root, text='Click me', command=lambda:store.trigger()).pack()
	# root.bind("<KeyRelease>",store.trigger())
	root.mainloop()