import Image
import ImageOps
import os

def scale_img(img, req_size):
    img = Image.open(img)
    original_ar = img.size[0]/float(img.size[1])

    if original_ar <= 1:
        h = int(req_size[1])
        w = int(req_size[1] * original_ar)
    else:
        w = int(req_size[0])
        h = int(req_size[0] * 1/original_ar)
    
    return ImageOps.fit(img, (w,h), Image.ANTIALIAS)

def get_image_paths(directory):
    '''return a list of image file paths from a directory'''
    fp = os.path.realpath(os.path.expanduser(directory))
    if not os.path.isdir(fp):
        raise OSError("Path is not a directory", fp)
    imgs = []
    import imghdr
    for file in os.listdir(fp):
        file = os.path.join(fp, file)
        if os.path.isdir(file):
            continue
        try:
            img_format = imghdr.what(file)
        except IOError:
            print 'Cannot open file {0} Continuing...'.format(file)
        else:
            if img_format:
                imgs.append(file)
            else:
                print 'File {0} not recognized as image Continuing...'.format(file)
    return imgs
