import os
from reportlab.lib import pagesizes
from reportlab.pdfgen import canvas

from imgs2pdf.core.helper import scale_img

class PDFOut(object):
    def __init__(self, filename, imgs, pagesize=pagesizes.A4, 
                 pageCompression=0, verbosity=0, password=None):
        fp = os.path.realpath(os.path.expanduser(filename))
        if os.path.isdir(fp):
            raise OSError("path is a directory", fp)
        dir_ = os.path.dirname(fp)
        if not os.access(dir_, os.W_OK):
            raise OSError("cannot write to directory", dir_)
        self.page_canvas = canvas.Canvas(fp, pagesize=pagesize,
                                pageCompression=pageCompression, 
                                verbosity=verbosity,
                                encrypt=password if type(password) is str or 
                                    password == None else None)
        self.pagesize = pagesize
        self.images = imgs
        
    @property
    def num_pages(self):
        return len(self.images)
        
    def savepdf(self):
        for img in self.images:
            img = scale_img(img, self.pagesize)
            self.page_canvas.drawInlineImage(img, 
                                self.pagesize[0]/2 - img.size[0]/2,
                                self.pagesize[1]/2 - img.size[1]/2)
            self.page_canvas.showPage()
        self.page_canvas.save()

