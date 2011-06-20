from Tkinter import *
from ttk import *
from tkFileDialog import Open, Directory, SaveAs
from threading import Thread

from imgs2pdf.core.helper import get_image_paths
from imgs2pdf.core.pdfout import PDFOut
from imgs2pdf.gui.progressbar import ProgressBarDialog

class MainWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        
        # treeview attributes
        self._item_num = 0
        self._swap_item = None
        
        self.grid(sticky=N+S+E+W)
        self.build_gui()
        master.config(menu=self.menubar)
    
    def build_gui(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        self.menubar = Menu(self)
        
        self.openmenu = Menu(self.menubar, tearoff=0)
        self.openmenu.add_command(label="Add files...",
                                  command=self.add_image_file)
        self.openmenu.add_command(label="Add from directory...",
                                  command=self.add_from_directory)
        self.menubar.add_cascade(label="Add images...", menu=self.openmenu)
        
        self.menubar.add_command(label="Save PDF...", command=self.save_pdf)
        self.menubar.add_command(label="Quit", command=self.quit)
        
        self.view = Treeview(self, selectmode="extended", show="headings",
                             columns=("page#", "file"))
        self.view.column("page#", width=100)
        self.view.column("file", width=500)
        self.view.heading(column="page#", text="Page#")
        self.view.heading(column="file", text="File")
        
        self.view.bind("<Delete>", self.delete_selected)
        self.view.bind('<B1-Motion>', self.drag_item_swap)
        self.view.bind('<ButtonRelease-1>', self.drop_item_swap)
        self.view.grid(row=0, column=0, sticky=N+S+E+W)
        
    def add_image_file(self):
        open_dialog = Open(self, initialdir='~')
        fp = open_dialog.show()
        if fp:
            self._item_num += 1
            self.view.insert('', END, values=('{0}'.format(self._item_num), fp))
    
    def add_from_directory(self):
        open_dialog = Directory(self)
        dirpath = open_dialog.show()
        if dirpath:
            imp = get_image_paths(dirpath)
            for fp in imp:
                self._item_num += 1
                self.view.insert('', END, values=('{0}'.format(self._item_num), fp))
        
    def delete_selected(self, event):
        items = self.view.selection()
        for item in items:
            self._delete_item(item)
        
    def drag_item_swap(self, event):
        if not self._swap_item:
            self._swap_item = self.view.identify_row(event.y)
    
    def drop_item_swap(self, event):
        if not self._swap_item:
            return
        item = self.view.identify_row(event.y)
        self._swap_file_values(item, self._swap_item)
        self.view.selection_set(item)
        self._swap_item = None

    def _delete_item(self, item):
        if not item:
            return
        nextitem = item
        nextnum = int(self.view.set(nextitem)['page#'])
        while nextnum != self._item_num:
            nextitem = self.view.next(nextitem)
            self.view.set(nextitem, "page#", value='{0}'.format(nextnum))
            nextnum += 1
        self.view.delete(item)
        self._item_num -= 1
        
    def _swap_file_values(self, item1, item2):
        f1 = self.view.set(item1)['file']
        f2 = self.view.set(item2)['file']
        if f1 == f2:
            return
        self.view.set(item1, column='file', value=f2)
        self.view.set(item2, column='file', value=f1)
        
    def save_pdf(self):
        img_paths = []
        items = self.view.get_children()
        for item in items:
            img_paths.append(self.view.set(item)['file'])
        save_dialog = SaveAs(self, initialdir='~')
        pdffp = save_dialog.show()
        pdf = PDFOut(pdffp, img_paths)
        pb_dialog = ProgressBarDialog(self, title='Saving to PDF...')
        pb_dialog.start()
        action_thread = Thread(target=pdf.savepdf)
        action_thread.start()
        # /home/tvrtko/downloads/pics
        def wait_to_finish():
            if not action_thread.isAlive():
                pb_dialog.destroy()
            else:
                self.after(100, wait_to_finish)
        self.after(100, wait_to_finish)
        self.wait_window(pb_dialog)
