'''
Created on May 23, 2023

@author: dan
'''

from PIL import Image, ImageDraw
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from random import sample,random, uniform, shuffle


def ellipse(output_path):
    image = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(image)
    draw.ellipse((25, 50, 175, 200), fill="red")
    draw.ellipse((100, 150, 275, 300), outline="black", width=5,
                 fill="yellow")
    image.save(output_path)
    
def rectangle(output_path):
    image = Image.new("RGB", (400, 400), "green")
    draw = ImageDraw.Draw(image)
    draw.rectangle((200, 100, 300, 200), fill="red")
    draw.rectangle((50, 50, 150, 150), fill="green", outline="yellow", width=3)
    image.save(output_path)

def make_bb(x, y, w, h=0):
    ''' 
    make bounding box around the point x,y. 
    Box has width, height w,h. If h==0, then h=w.
    '''
    ww = w/2
    if h==0: 
        hh = ww 
    else:
        hh = h/2
    b = (x-ww, y-hh, x+ww, y+hh)
    return b
    
def draw_conte_cue(draw, t):
    '''
    draw a blob of dots centered at cue_x, cue_y. 
    The blob has diameter cue_diameter, and the dots have
    diameter dot_diameter.
    '''
    (cue_x, cue_y, cue_diam, dot_diam, nred, ngreen) = t
    fill_colors = ["red"]*nred + ["green"]*ngreen
    shuffle(fill_colors)
    for c in fill_colors:
        # count = 0
        # while count < (nred+ngreen):
        # look for point inside unit circle
        x = uniform(-1, 1)
        y = uniform(-1, 1)
        if x*x + y*y < 1:
            xdot = cue_x + x*cue_diam/2
            ydot = cue_y + y*cue_diam/2
            draw.ellipse(make_bb(xdot, ydot, dot_diam), fill=c)
    
def make_image(w_image, h_image, filename, tuple_or_list):
    if isinstance(tuple_or_list, tuple) and len(tuple_or_list)==6:
        list_of_tuples = [tuple_or_list]
    elif isinstance(tuple_or_list, list) and all(isinstance(z, tuple) and len(z)==6 for z in tuple_or_list):
        list_of_tuples = tuple_or_list
    elif tuple_or_list is None:
        list_of_tuples = []

    # create image
    image = Image.new("RGB", (w_image, h_image), "gray")
    draw = ImageDraw.Draw(image)

    for tup in list_of_tuples:
        #print('draw tuple: ', tup)
        draw_conte_cue(draw, tup)

    # # splat
    # count = 0
    # while count < (nr+nb):
    #     x = uniform(-1, 1)
    #     y = uniform(-1, 1)
    #     if x*x + y*y < 1:
    #         if count < nr:
    #             fill_color="red"
    #         else:
    #             fill_color="green"
    #         xdot = xc + x*qradpx
    #         ydot = yc + y*qradpx
    #         draw.ellipse((xdot-radpx, ydot-radpx, xdot+radpx, ydot+radpx), fill=fill_color)
    #         count = count + 1

    image.save(filename)
    
    
    
    
    
if __name__ == "__main__":
    #rectangle("rectangle.jpg")
    #ellipse("ellipse.png")
    
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-W", "--width-degrees", dest="width_degrees", type=int, required=False, default=30, help="width of image in visual degrees")
    #parser.add_argument("-r", "--red", dest="n_red", type=int, default=10, required=False, help="Number of red dots")
    #parser.add_argument("-b", "--blue", dest="n_blue", type=int, default=10, required=False, help="Number of blue dots")
    parser.add_argument("-m", "--dot-diameter", dest="dot_diameter", type=float, default=1, required=False, help="diameter of each dot in visual degrees")
    parser.add_argument("-q", "--cue-diameter", dest="cue_diameter", type=float, default=6, required=False, help="diameter of cue region")
    parser.add_argument("-o", "--output", dest="output", required=False, help="output filename pattern, no extension!")
    parser.add_argument("-n", "--num-images", dest="num_images", required=False, type=int, default=1, help="number of images to create")
    parser.add_argument("-N", "--num-dots", dest="num_dots", required=False, type=int, default=100, help='number of dots per cue')
    parser.add_argument("-B", "--num-buffer", dest="num_buffer", required=False, type=int, default=0, help="Number of pre- and post- buffer bkgd images")
    # Process arguments
    args = parser.parse_args()

    # definitions
    w = 1024
    h = 768
    ppd = 1024/args.width_degrees
    dot_diam_px = ppd * args.dot_diameter
    cue_diam_px = ppd * args.cue_diameter
    print(cue_diam_px, dot_diam_px)
    
    l = []
    l.append((w/4, h/4, cue_diam_px, dot_diam_px/2, round(.75 * args.num_dots), round(.25 * args.num_dots)))
    l.append((2*w/4, h/4, cue_diam_px, dot_diam_px/2, round(.5 * args.num_dots), round(.5 * args.num_dots)))
    l.append((3*w/4, h/4, cue_diam_px, dot_diam_px/2, round(.25 * args.num_dots), round(.75 * args.num_dots)))

    l.append((w/4, h/2, cue_diam_px, dot_diam_px, round(.75 * args.num_dots), round(.25 * args.num_dots)))
    l.append((2*w/4, h/2, cue_diam_px, dot_diam_px, round(.5 * args.num_dots), round(.5 * args.num_dots)))
    l.append((3*w/4, h/2, cue_diam_px, dot_diam_px, round(.25 * args.num_dots), round(.75 * args.num_dots)))

    l.append((w/4, 3*h/4, cue_diam_px, 2*dot_diam_px, round(.75 * args.num_dots), round(.25 * args.num_dots)))
    l.append((2*w/4, 3*h/4, cue_diam_px, 2*dot_diam_px, round(.5 * args.num_dots), round(.5 * args.num_dots)))
    l.append((3*w/4, 3*h/4, cue_diam_px, 2*dot_diam_px, round(.25 * args.num_dots), round(.75 * args.num_dots)))

    # create pre-buffer
    for i in range(args.num_buffer):
        filename = f'{args.output}-{i:03d}.png'       
        make_image(w, h, filename, None)
    
    # create images
    for i in range(args.num_images): 
        filename = f'{args.output}-{i+args.num_buffer:03d}.png'       
        #make_image(w, h, filename, (w/2, h/2, cue_diam_px, dot_diam_px, args.n_red, args.n_blue))
        make_image(w, h, filename, l)

    # create post-buffer
    for i in range(args.num_buffer):
        filename = f'{args.output}-{i+args.num_buffer+args.num_images:03d}.png'       
        make_image(w, h, filename, None)
