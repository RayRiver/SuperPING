#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import Tkinter as tk
import ttk


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack(expand=tk.YES, fill=tk.BOTH)

        table = ttk.Treeview(self, columns=('name', 'ip', 'delay'))
        table.column('name', width=100, anchor='center')
        table.column('ip', width=300, anchor='center')
        table.column('delay', width=100, anchor='center')
        table.heading('name', text='VPN线路')
        table.heading('ip', text='IP地址')
        table.heading('delay', text='延迟')
        table.pack(expand=tk.YES, fill=tk.BOTH)

        for i in range(10):
            table.insert('', i, values=("xunda", "j1.xunda.com", "98 ms"))


    def process_directory(self, parent, path):
        # 遍历路径下的子目录
        for p in os.listdir(path):
            # 构建路径
            abspath = os.path.join(path, p)
            # 是否存在子目录
            isdir = os.path.isdir(abspath)
            oid = self.tree.insert(parent, 'end', text=p, open=False)
            if isdir:
                self.process_directory(oid, abspath)


def t():
    root = tk.Tk()
    tree = ttk.Treeview(root, columns=('col1','col2','col3'))
    tree.column('col1', width=100, anchor='center')
    tree.column('col2', width=100, anchor='center')
    tree.column('col3', width=100, anchor='center')
    tree.heading('col1', text='col1')
    tree.heading('col2', text='col2')
    tree.heading('col3', text='col3')
    def onDBClick(event):
        item = tree.selection()[0]
        print "you clicked on ", tree.item(item, "values")

    for i in range(10):
        tree.insert('',i,values=('a'+str(i),'b'+str(i),'c'+str(i)))
    tree.bind("<Double-1>", onDBClick)

    tree.pack()
    root.mainloop()


def create_menu(root):
    menu = tk.Menu(root)

    file_menu = tk.Menu(menu, tearoff=0)
    file_menu.add_command(label = "Quit", command=root.quit)
    menu.add_cascade(label="File", menu=file_menu)

    return menu


def main():
    if False:
        t()
    else:
        root = tk.Tk()
        root.title("Super PING")
        root.geometry('640x480')

        menubar = create_menu(root)
        root.config(menu=menubar)

        app = App(root)

        root.mainloop()


if __name__ == '__main__':
    main()
