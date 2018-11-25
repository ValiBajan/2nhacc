import tkinter as tk
import os
from tkinter.filedialog import askopenfilename
import process_nii
from PIL import Image, ImageTk

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
xCrop = [30, 122, 175, 285, 345, 440]
yCrop = [50, 138, 50, 140, 45, 155]

class Browse(tk.Frame):

    def __init__(self, master, initialdir='', filetypes=()):
        #tk.Toplevel( width=400, height=100 )
        super().__init__(master)
        self.filepath = tk.StringVar()
        self._initaldir = initialdir
        self._filetypes = filetypes
        self._create_widgets()
        self._display_widgets()

    def _create_widgets(self):
        self._entry = tk.Entry(self, textvariable=self.filepath)
        self._entry.pack()
        self._button = tk.Button(self,  text="Browse", command=self.browse)
        self._button.pack()
        self._button = tk.Button(self, text='Analyze', fg='red', command = self.analyze)
        self._button.pack()
        self._button = tk.Button(self, text='Results', command = self.new_window)
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

    def browse(self):
        self.filepath = askopenfilename(filetypes=(("MRI Scan", "*.nii"),
                                             ("All files", "*.*") ))

    def analyze(self):
        #os.chdir('C:/2NHack/Dataset/')
        #niiFile = os.path.relpath(niiFile)
        #niiFile = os.path.relpath(niiFile)
        print(self.filepath)
        self.filepath = os.path.relpath(self.filepath)ss
        if (os.path.isfile(self.filepath)):
            process_nii.nii2jpg(inFile=self.filepath, outFile='brain.jpg')
            process_nii.splitAndConvert(inFile='brain.jpg', fileNumber='', gray=True, xCrop=xCrop, yCrop=yCrop)
        else:
            print ('Incorrect file path')
            
    def new_window(self):
        self._top = tk.Toplevel()
        self._img = ImageTk.PhotoImage(Image.open('brain.jpg'))
        self._imgLabel = tk.Label(self, image=self._img)
        self._imgLabel.pack(side='bottom', fill='both', expand='yes')
        self._resLabel = tk.Label(self, text='Probabilitate schizofrenie: 100%')
        self._resLabel.pack(side='bottom', fill='both', expand='yes')
        

if __name__ == "__main__": 
    root = tk.Tk()
    file_browser = Browse(root, initialdir=str(os.getcwd()))
    file_browser.pack(fill='x', expand=True)
    
    
    
    root.mainloop()