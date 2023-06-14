#!/usr/bin/env python
import PySimpleGUI as sg
import random
import string
import operator


def your_function_for_mqtt():
    # lol tutaj piszecie
    print("cos, by bylo")
#

def modulo(index):
    return index % 4 + 1


def new_measure(window, data, index, measurement_number):
    additional_int = 0
    if index == 3:
        additional_int = 1
    if index == 4:
        measurement_number += 1

    your_function_for_mqtt()
    new_index = modulo(index)
    rand = random.randint(1, 100)
    new_measure = [f"{measurement_number}", f"Gracz {new_index}", rand]
    data.append(new_measure)
    window["-TABLE-"].update(values=data)
    window["-ACTUAL-GAMER-TEXT-"].update(value=f"Actual gamer: Gamer {modulo(new_index)}")
    window["-ACTUAL-ROUND-TEXT-"].update(value=f"Actual round: {measurement_number + additional_int}")

    return new_index, measurement_number
# sg.theme('Light green 6')


index = 4
measurement_number = 1
headings = ["Game number", "Gamer name", "Measurement"]
data = [
    ["1", "Gracz 1", 21],
    ["1", "Gracz 2", 20],
    ["1", "Gracz 3", 24],
    ["1", "Gracz 4", 25]
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
          [sg.Text("Actual gamer: Gamer 1", key="-ACTUAL-GAMER-TEXT-")],
          [sg.Text("Current round: 2", key="-ACTUAL-ROUND-TEXT-")],
          [sg.Button("Start", key="-START-STOP-"), sg.Button('Next gamer', key="-ADD-", button_color="blue")],
          [sg.Button('EXIT', key="-EXIT-", button_color="red")],
          ],

window = sg.Window('The Table Element', layout,
                    size = (600, 600),
                   element_justification='c',
                   resizable=True, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT, finalize=True)

window.bind("<space>", "-SPACE-KEY-")
window.force_focus()

while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == '-EXIT-':
        break
    if event in ["-ADD-", "-SPACE-KEY-"]:
        index, measurement_number = new_measure(window, index=index, data=data, measurement_number=measurement_number)

window.close()
