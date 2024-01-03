import tkinter as tk 
from tkinter import ttk
from datetime import datetime
from tkinter import messagebox
import sqlite3 as sq
from turtle import width

root = tk.Tk()
root.title("To-Do App")
root.geometry("1100x600+500+100")
root.configure(background='#282828')

conn = sq.connect(r'todo.db')
cur = conn.cursor()
cur.execute('create table if not exists tasks (title text, time datetime, status text)')

task = []

def addTask():
    word = e1.get()
    if len(word) == 0:
        messagebox.showinfo("Empty Entry", "Please enter task name")
    
    else:
        time = str(datetime.now()).split(".")[0]
        task.append([word, time, 'F'])
        cur.execute("insert into tasks (title, time, status) values (?,?,?)", (word, time, "F"))
        listUpdate()
        e1.delete(0, 'end')

def listUpdate():
    clearList()
    retrieveDB()
    for i in task:
        if i[2] == "T":
            tree.insert('', 'end', "checked",values=(i[0], i[1]))
        else:
            tree.insert('', 'end', "unchecked",values=(i[0], i[1]))

def delOne():
    try:
        val = tree.selection()[0]
        curItem = tree.focus()
        cur.execute("delete from tasks where title = ? and time = ?", (tree.item(curItem)["values"][0],tree.item(curItem)["values"][1]))
        tree.delete(val)

    except:
        messagebox.showinfo("Can't Delete", "No Task Selected")

def deleteAll():
    mb = messagebox.askyesno("Delete All", "Are you sure?")
    if mb == True:
        while(len(task)!=0):
            task.pop()
        cur.execute("delete from tasks")
        listUpdate()

def checkAll():
    mb = messagebox.askyesno("Check All", "Are you sure?")
    if mb == True:
        cur.execute("UPDATE tasks SET status = 'T'")
        listUpdate()

def uncheckAll():
    mb = messagebox.askyesno("Check All", "Are you sure?")
    if mb == True:
        cur.execute("UPDATE tasks SET status = 'F'")
        listUpdate()

def clearList():
    for row in tree.get_children():
        tree.delete(row)

def bye():
    root.destroy()

def retrieveDB():
    while(len(task)!=0):
        task.pop()
    for row in cur.execute("select * from tasks"):
        task.append([row[0],row[1].split(".")[0], row[2]])


class CbTreeview(ttk.Treeview):
    def __init__(self, master=None, **kw):
        kw.setdefault('style', 'cb.Treeview')
        kw.setdefault('show', 'headings')  # hide column #0
        ttk.Treeview.__init__(self, master, **kw)
        # create checheckbox images
        self._im_checked = tk.PhotoImage('checked',
                                         data=b'GIF89a\x0e\x00\x0e\x00\xf0\x00\x00\x00\x00\x00\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x0e\x00\x0e\x00\x00\x02#\x04\x82\xa9v\xc8\xef\xdc\x83k\x9ap\xe5\xc4\x99S\x96l^\x83qZ\xd7\x8d$\xa8\xae\x99\x15Zl#\xd3\xa9"\x15\x00;',
                                         master=self)
        self._im_unchecked = tk.PhotoImage('unchecked',
                                           data=b'GIF89a\x0e\x00\x0e\x00\xf0\x00\x00\x00\x00\x00\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x0e\x00\x0e\x00\x00\x02\x1e\x04\x82\xa9v\xc1\xdf"|i\xc2j\x19\xce\x06q\xed|\xd2\xe7\x89%yZ^J\x85\x8d\xb2\x00\x05\x00;',
                                           master=self)
        style = ttk.Style(self)
        style.configure("cb.Treeview.Heading", font=(None, 13))
        # put image on the right
        style.layout('cb.Treeview.Row',
                     [('Treeitem.row', {'sticky': 'nswe'}),
                      ('Treeitem.image', {'side': 'right', 'sticky': 'e'})])

        # use tags to set the checkbox state
        self.tag_configure('checked', image='checked')
        self.tag_configure('unchecked', image='unchecked')

    def tag_add(self, item, tags):
        new_tags = tuple(self.item(item, 'tags')) + tuple(tags)
        self.item(item, tags=new_tags)

    def tag_remove(self, item, tag):
        tags = list(self.item(item, 'tags'))
        tags.remove(tag)
        self.item(item, tags=tags)

    def insert(self, parent, index, tags, iid=None, **kw ):
        item = ttk.Treeview.insert(self, parent, index, iid, **kw)
        self.tag_add(item, (item, tags))
        self.tag_bind(item, '<ButtonRelease-1>',
                      lambda event: self._on_click(event, item))

    def _on_click(self, event, item):
        """Handle click on items."""
        if self.identify_row(event.y) == item:
            if self.identify_column(event.x) == '#3': # click in 'Served' column
                # toggle checkbox image
                if self.tag_has('checked', item):
                    curItem=self.focus()
                    cur.execute("UPDATE tasks SET status = 'F' where title = ? and time = ?", (tree.item(curItem)["values"][0],tree.item(curItem)["values"][1]))
                    self.tag_remove(item, 'checked')
                    self.tag_add(item, ('unchecked',))

                else:
                    curItem=self.focus()
                    cur.execute("UPDATE tasks SET status = 'T' where title = ? and time = ?", (tree.item(curItem)["values"][0],tree.item(curItem)["values"][1]))
                    self.tag_remove(item, 'unchecked')
                    self.tag_add(item, ('checked',))

tree = CbTreeview(root, columns=("Title", "Time", "Served"),
                  height=20, selectmode="extended")

tree.heading('Title', text="Title", anchor=tk.CENTER)
tree.heading('Time', text="Time", anchor=tk.CENTER)
tree.heading('Served', text="Status", anchor=tk.CENTER)
tree.column('#1', stretch='no', minwidth=0, width=350)
tree.column('#2', stretch='no', minwidth=0, width=150)
tree.column('#3', stretch='no', minwidth=0, width=70)
tree.pack(fill='both')
tree.place(x=440, y = 100)

l1 = ttk.Label(root, text = 'To-Do List', background= "#282828", foreground= "white", font= "Times 20 bold")
l2 = ttk.Label(root, text='Enter task title: ', background= "#282828", foreground= "white", font= "Arial 10 bold")
e1 = ttk.Entry(root, width=41,)
# t = tk.Listbox(root, height=22, selectmode='SINGLE',width= 50)
b1 = ttk.Button(root, text='Add task', width=40, command=addTask,)
b2 = ttk.Button(root, text='check all', width=40, command=checkAll)
b3 = ttk.Button(root, text='uncheck all', width=40, command=uncheckAll)
b4 = ttk.Button(root, text='Delete', width=40, command=delOne)
b5 = ttk.Button(root, text='Delete all', width=40, command=deleteAll)
b6 = ttk.Button(root, text='Exit', width=40, command=bye)

retrieveDB()
listUpdate()

l2.place(x=100, y=130)
e1.place(x=100, y=160)
b1.place(x=100, y=220)
b2.place(x=100, y=260)
b3.place(x=100, y=300)
b4.place(x=100, y=340)
b5.place(x=100, y=380)
b6.place(x=100, y=420)
l1.place(x=100, y=20)

root.mainloop()
    
conn.commit()
cur.close()