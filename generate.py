#!/usr/bin/env python




import sys
import cairo
import rsvg
import gtk
import math



DEG_TO_RAD = 2.0*3.14159/360.0

WIDTH, HEIGHT  = 800, 800

#		old style	new style
#
#face		50-72		0-58
#hour l		296		263
#minute l	380		375
#second l	393		375
#h w		23		19
#m w		20		14
#s w		9		9
#mark inner	275		293,296
#mark outer	375		375
#mark gap	9		16
#mark width	8-34
#mark colour	3ea1e2		3a64ac
#hands colour	3ea1e2		d9c066

BLUE = "#3a64ac"
GOLD = "#d9c066"


def makeit(name, function):
    fo = file("clock-"+name+".svg", 'w')

    

    ## Prepare a destination surface -> out to an SVG file!
    surface = cairo.SVGSurface (fo, 80, 80)

    ## draw something - this taken from the web.
    ctx = cairo.Context (surface)

    #ctx.scale (WIDTH/100, HEIGHT/100) # Normalizing the canvas
    ctx.set_source_rgba(0.0, 0.0, 0.0, 0.0) 
    ctx.set_operator(cairo.OPERATOR_SOURCE)
    ctx.paint()
    ctx.scale(80.0/WIDTH, 80.0/HEIGHT);

    function(ctx)

    #ctx.rectangle (0, 0, 400, 400) # Rectangle(x0, y0, x1, y1)
    
    #ctx.fill ()

    ## Do the deed.
    surface.finish()
    fo.close()

# utility functions

def centre(ctx):
    ctx.translate(WIDTH/2,HEIGHT/2)
    
def rect_by_rad_w(inner, outer, width, ctx):
    ctx.rectangle(-width/2.0, inner, width, outer-inner)
    
    ctx.fill()

def double_rect_by_rad_w(inner, outer, width, gap, ctx):
    ctx.rectangle(((-gap/2.0)-width), inner, width, outer-inner)
    ctx.rectangle(gap/2.0, inner, width, outer-inner)
    
    ctx.fill()

def set_source_hex(colour, ctx):
    assert(len(colour) == 7)
    assert(colour[0] == '#')
    r = int(colour[1:3], 16)
    g = int(colour[3:5], 16)
    b = int(colour[5:7], 16)
    ctx.set_source_rgba(r/255.0, g/255.0, b/255.0, 1.0)


# the generators

def drop_shadow(ctx):
    ctx.set_source_rgba(0.0, 0.0, 0.0, 0.95) 
    ctx.set_operator(cairo.OPERATOR_SOURCE)
    ctx.rectangle(0, 0, WIDTH, HEIGHT)
    ctx.fill()

def marks(ctx):
    centre(ctx)

    set_source_hex(BLUE, ctx) 
    ctx.set_operator(cairo.OPERATOR_SOURCE)

    for i in range(12):
        if (i % 3) == 0:
            double_rect_by_rad_w(296, 375, 23, 14, ctx)
        else:
            rect_by_rad_w(296, 375, 23, ctx)
        ctx.rotate(30*DEG_TO_RAD)

def hour_hand(ctx):
    ctx.rotate(-90*DEG_TO_RAD)
    set_source_hex(GOLD, ctx) 
    ctx.set_operator(cairo.OPERATOR_SOURCE)
    rect_by_rad_w(58, 263, 19, ctx)

def minute_hand(ctx):
    ctx.rotate(-90*DEG_TO_RAD)
    set_source_hex(GOLD, ctx) 
    ctx.set_operator(cairo.OPERATOR_SOURCE)
    rect_by_rad_w(58, 375, 14, ctx)

def second_hand(ctx):
    ctx.rotate(-90*DEG_TO_RAD)
    set_source_hex(GOLD, ctx) 
    ctx.set_operator(cairo.OPERATOR_SOURCE)
    rect_by_rad_w(58, 375, 9, ctx)

def nop(ctx):
    pass

def main():
    makeit("drop-shadow", drop_shadow)
    makeit("face-shadow", nop)
    makeit("face", nop)
    makeit("frame", nop)
    makeit("glass", nop)
    makeit("marks", marks)

    makeit("hour-hand", hour_hand)
    makeit("hour-hand-shadow", nop)
    makeit("minute-hand", minute_hand)
    makeit("minute-hand-shadow", nop)
    makeit("second-hand", second_hand)
    makeit("second-hand-shadow", nop)



if __name__ == '__main__':
    main()
