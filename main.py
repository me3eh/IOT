#!/usr/bin/env python
import PySimpleGUI as sg
import random
import string
import operator

# sg.theme('Light green 6')

headings = ["Nazwa Gracza", "Pomiar1"]

data = [
    ["Gracz 1", 21],
    ["Gracz 2", 20],
    ["Gracz 3", 24],
    ["Gracz 4", 25]
]

layout = [[sg.Table(values=data[0:][:],
                    headings=headings,
                    max_col_width=4,
                    auto_size_columns=True,
                    display_row_numbers=False,
                    justification='right',
                    right_click_selects=True,
                    key='-TABLE-',
                    enable_events=True,
                    expand_x=True,
                    expand_y=True,
                    enable_click_events=True,           # Comment out to not enable header and other clicks
                    tooltip='This is a table')],
          [sg.Button('Add new value', key="-ADD-"), sg.Button('EXIT', key="-EXIT-")],
          [sg.Button("Start", key="-START-STOP-"), sg.Button('Next gamer', key="-NEXT-")]
    ],

window = sg.Window('The Table Element', layout,
                   # ttk_theme='clam',
                   resizable=True, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT, finalize=True)

# window["-TABLE-"].bind('<Double-Button-1>' , "+-double click-")
index = 0
while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == '-EXIT-':
        break
    if event == "-ADD-":
        index += 1
        # data[0].append("40")
        # data[1].append("40")
        # data[2].append("40")
        # data[3].append("40")
        l = ["Gracz 4", 25]
        # print(window["-TABLE-"])
        data = data + l
        print(data)
        window["-TABLE-"].update(values=data)
window.close()
