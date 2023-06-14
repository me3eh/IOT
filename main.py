#!/usr/bin/env python
import time
import paho.mqtt.client as mqtt
import PySimpleGUI as sg
import random
import string
import operator

mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic_esp_status = "esp32/status"
mqtt_topic_esp_value = "esp32/value"
mqtt_topic_ev3 = "ev3/move"
player_values = [300, 300, 300, 300]
username = ""
password = ""


# def main_window():
def layout():
    return [[sg.Table(values=data[0:][:],
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
                      enable_click_events=True,  # Comment out to not enable header and other clicks
                      tooltip='This is a table')],
            [sg.Text("Actual gamer: Gamer 1", key="-ACTUAL-GAMER-TEXT-")],
            [sg.Text("Current round: 2", key="-ACTUAL-ROUND-TEXT-")],
            [sg.Button("Stop", key="-EXIT-", button_color="red"),
             sg.Button('Next gamer', key="-ADD-", button_color="blue")],
            [sg.Button('Theme', key='-THEME-')],
            ]


def mqtt_function(index):
    print("MQTT function:")

    def on_connect(client, userdata, flags, rc):
        print("Połączono z MQTT brokerem")
        client.subscribe(mqtt_topic_esp_value)

    def on_message(client, userdata, msg):
        message = msg.payload.decode()
        nonlocal alcohol_value
        print("Received value from ESP32: " + message)
        alcohol_value = int(message)

    alcohol_value = None
    temp = 0
    client = mqtt.Client()
    # client.username_pw_set(username=username, password=password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_broker, mqtt_port, 60)
    client.publish(mqtt_topic_esp_status, "start")

    client.loop_start()
    while alcohol_value is None:
        temp = 1

    if alcohol_value < player_values[index - 1]:
        print("gracz" + str(index) + " MNIEJ pijany")
        client.publish(mqtt_topic_ev3, "gracz" + str(index))
        player_values[index - 1] = alcohol_value
    else:
        print("gracz" + str(index) + " dalej pijany")

    client.loop_stop()
    client.disconnect()

    if alcohol_value < player_values[index - 1]:
        return [f"{measurement_number}", f"Gracz {index}", alcohol_value]
    else:
        return [f"{measurement_number}", f"Gracz {index}", player_values[index - 1]]


def modulo(index):
    return index % 4 + 1


def new_measure(window, data, index, measurement_number):
    additional_int = 0
    if index == 3:
        additional_int = 1
    if index == 4:
        measurement_number += 1

    new_index = modulo(index)
    new_measurement = mqtt_function(new_index)
    data.append(new_measurement)
    window["-TABLE-"].update(values=data)
    window["-ACTUAL-GAMER-TEXT-"].update(value=f"Actual gamer: Gamer {modulo(new_index)}")
    window["-ACTUAL-ROUND-TEXT-"].update(value=f"Actual round: {measurement_number + additional_int}")

    return new_index, measurement_number


# sg.theme('Light green 6')


index = 4
measurement_number = 1
headings = ["Game number", "Gamer name", "Measurement"]
data = [
    ["0", "Gracz 1", 300],
    ["0", "Gracz 2", 300],
    ["0", "Gracz 3", 300],
    ["0", "Gracz 4", 300]
]

window = sg.Window('The Table Element', layout(),
                   size=(600, 600),
                   element_justification='c',
                   resizable=True, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT, finalize=True)


def make_window():
    # Set theme based on previously saved
    sg.theme(sg.user_settings_get_entry('theme', None))

    return sg.Window('The Table Element', layout(),
                     size=(600, 600),
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

    if event == '-THEME-':  # Theme button clicked, so get new theme and restart window
        ev, vals = sg.Window('Choose Theme',
                             [[sg.Combo(sg.theme_list(), k='-THEME LIST-'), sg.OK(), sg.Cancel()]]).read(close=True)
        if ev == 'OK':
            window.close()
            sg.user_settings_set_entry('theme', vals['-THEME LIST-'])
            window = make_window()
window.close()
