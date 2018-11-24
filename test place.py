# -*- coding: utf-8 -*-

import sys
#from tkinter import *
#from tkinter import ttk
#from tkinter import filedialog
import tkinter as tk
from tkinter import filedialog as fd
class Root(Tk):

    self = Tk()
    """
    self.minsize(300, 300)
    self.title("v1")
    
    
    self.labelFrame = ttk.Labelframe( self, text = 'pls work')
    self.labelFrame.grid(column = 0, row = 1, padx = 10, pady = 20)
    """
    """
    self.button()
    
    def button(self):
        self.button = ttk.Button(self.labelFrame, text='Browse')
        self.button.grid(column = 1, row = 1)
    
    #self.button.pack()
    """
    """
    self.button( text = "Browse", command = self.loadtemplate, width = 10).pack()
    
    def loadtemplate(self): 
        filename = tkFileDialog.askopenfilename(filetypes = (("Template files", "*.tplate")
                                                             ,("HTML files", "*.html;*.htm")
                                                             ,("All files", "*.*") ))
        if filename: 
            try: 
                self.settings["template"].set(filename)
            except: 
                tkMessageBox.showerror("Open Source File", "Failed to read file \n'%s'"%filename)
                return
                
    """
    
    def __init__(self, master, initialdir='', filetypes=()):
        super().__init__(master)
        self.filepath = tk.StringVar()
        self._initaldir = initialdir
        self._filetypes = filetypes
        self._create_widgets()
        self._display_widgets()

    def _create_widgets(self):
        self._entry = tk.Entry(self, textvariable=self.filepath)
        self._button = tk.Button(self, text="Browse...", command=self.browse)

    def _display_widgets(self):
        self._entry.pack(fill='x', expand=True)
        self._button.pack(anchor='se')
    
    def browse(self):
        """ Browses a .png file or all files and then puts it on the entry.
        """

        self.filepath.set(fd.askopenfilename(initialdir=self._initaldir,
                                             filetypes=self._filetypes))



    self.mainloop()
    
if __name__ == '__main__':
    root = tk.Tk()

    file_browser = Browse(root, initialdir=r"C:\Users",
                                filetypes=(('Portable Network Graphics','*.png'),
                                                            ("All files", "*.*")))
    file_browser.pack(fill='x', expand=True)

    root.mainloop()