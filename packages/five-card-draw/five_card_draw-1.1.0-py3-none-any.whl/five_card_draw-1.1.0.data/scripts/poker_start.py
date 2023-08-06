'''Module ran to start the program, Poker: 5 Card Redraw'''

def init(top, gui, *args, **kwargs):
    '''Initialize globals for the top level of the GUI'''
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def destroy_window():
    '''Function which closes the window.'''
    global top_level
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
    from five_card_draw import fcd_pagegui
    fcd_pagegui.vp_start_gui()
