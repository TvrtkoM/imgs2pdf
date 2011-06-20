from Tkinter import Tk
from imgs2pdf.gui.main import MainWindow

def run():
    root = Tk()
    root.title("Imgs2PDF")
    root.geometry("%dx%d%+d%+d" % (600, 400, 0, 0))
    root.minsize(600, 400)
    app = MainWindow(master=root)
    
    app.mainloop()
    
if __name__ == '__main__':
    run()