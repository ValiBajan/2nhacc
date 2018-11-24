#import sys
import tkinter as tk
import os
from tkinter import *
from tkinter import filedialog as fd
import process_nii
#from tkinter import ttk
#from tkinter import filedialog
#os.chdir('C:\\2NHack')
curDir = str(os.getcwd())
xCrop = [30, 122, 175, 285, 345, 440]
yCrop = [50, 138, 50, 140, 45, 155]

class Browse(tk.Frame):
    """ Creates a frame that contains a button when clicked lets the user to select
    a file and put its filepath into an entry.
    """
    
    def __init__(self, master, initialdir='', filetypes=()):
        super().__init__(master)
        self.filepath = tk.StringVar()
        self._initaldir = initialdir
        self._filetypes = filetypes
        self._create_widgets()
        self._display_widgets()
                
    def _create_widgets(self):
        back = tk.Frame( width=400, height=200).pack()
        self._label = tk.Label(text='Ur mom gay', fg='blue')
        self._label.pack()
        self._entry = tk.Entry(self, textvariable=self.filepath)
        self._entry.pack()
        self._button = tk.Button(self,  text="Browse", command=self.browse)
        self._button.pack()
        self._button = tk.Button(self, text='Analyze', fg='red', command = self.chestie)
        self._button.pack()
        
    
    def _display_widgets(self):
        self._entry.pack(fill='x', expand=True)
        #self.browse()
        #data_folder = Path('{}\\'.format(curDir))
        #file_to_open = data_folder / "path.txt"
        #f = open(file_to_open, 'w+')
        #string = os.path.abspath("test_place.py")
        #f.write(file_browser.filepath.get())
        #f.close
        
    def chestie(self):
        if (os.path.isfile(niiFile)):
            process_nii.nii2jpg(inFile=niiFile, outFile='{}brain.jpg'.format(curDir))
            process_nii.splitAndConvert(inFile='{}brain.jpg'.format(curDir), outDir='{}'.format(curDir), fileNumber='', gray=True, xCrop=xCrop, yCrop=yCrop)
        else:
            print ('Incorrect file path')
    
    def browse(self):
        self.filepath.set(fd.askopenfilename(initialdir=self._initaldir,
                                             filetypes=self._filetypes))
        niiFile = file_browser.filepath.get()
        #niiFile = niiFile[18:]
        print(niiFile)
        
        
        
    
        
if __name__ == '__main__':
    #print(str(os.getcwd()))
    root = tk.Tk()
    
    file_browser = Browse(root, initialdir=str('{}\\'.format(curDir)),
                                filetypes=(('NII','*.nii'),
                                                            ("All files", "*.*")))
    file_browser.pack(fill='x', expand=True)
    #if (os.path.isfile(niiFile)):
    #    process_nii.nii2jpg(inFile=niiFile, outFile='{}brain.jpg'.format(curDir))
    #    process_nii.splitAndConvert(inFile='{}brain.jpg'.format(curDir), outDir='{}'.format(curDir), fileNumber='', gray=True, xCrop=xCrop, yCrop=yCrop)
    #else:
    #   print ('Incorrect file path')
    
    root.mainloop()