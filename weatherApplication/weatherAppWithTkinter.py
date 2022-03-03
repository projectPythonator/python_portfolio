from configparser import ConfigParser
from tkinter import Button, Entry, Label, StringVar, Tk, messagebox

import requests

KELVIN_CONST = 273.15


class LabelPack:
    def __init__(self, parent_window, label_text, font_settings, bg_colour):
        self.label_info = Label(
            parent_window, text=label_text, font=font_settings, bg=bg_colour
        )
        self.label_info.pack()

    def set_by_key(self, key_str, set_value):  # put guards
        self.label_info[key_str] = set_value


class EntryPack:
    def __init__(self, parent_window, message, font_settings, fg_colour):
        self.entry_info = Entry(
            parent_window,
            textvariable=message,
            font=font_settings,
            fg=fg_colour,
        )
        self.entry_info.pack()


class ButtonPack:
    def __init__(
        self,
        parent_window,
        button_text,
        font_settings,
        fg_colour,
        bg_colour,
        button_command,
        button_size,
    ):
        self.button_info = Button(
            parent_window,
            text=button_text,
            width=button_size,
            fg=fg_colour,
            bg=bg_colour,
            font=font_settings,
            command=button_command,
        )
        self.button_info.pack()


class APIData:
    def __init__(self, url_string):
        self.url_api = url_string
        self.api_key = None

    def grab_api_key(self, file_path):
        file_stream = ConfigParser()
        file_stream.read(file_path)
        self.api_key = file_stream["api_key"]["key"]
        file_stream.close()

    def find_weather_by_city(self, city_name):
        api_report = requests.get(self.url_api.format(city_name, self.api_key))
        if api_report:
            weather_json = api_report.json()
            town_name = weather_json["name"]
            country_name = weather_json["sys"]["country"]
            kelvins = weather_json["main"]["temp"]
            celsius = kelvins - KELVIN_CONST
            fahrenheit = celsius * 9 / 5 + 32
            weather_status = weather_json["weather"][0]["main"]
            return (
                town_name,
                country_name,
                celsius,
                fahrenheit,
                weather_status,
            )
        else:
            return None


class AppWindow:
    def __init__(self, window_title, window_colour, window_size, api_pack):
        self.app_window = Tk()
        self.app_window.title(window_title)
        self.app_window.configure(bg=window_colour)
        self.app_window.geometry(window_size)
        self.api_data = api_pack
        self.label_map = {}
        self.entry_map = {}
        self.button_map = {}
        self.text_grabber = StringVar()

    def fill_labels(self):
        self.label_map["location"] = LabelPack(
            self.app_window, "", ("Arial", 35, "bold"), "lightblue"
        )
        self.label_map["temperature"] = LabelPack(
            self.app_window, "", ("Arial", 35, "bold"), "lightpink"
        )
        self.label_map["weather"] = LabelPack(
            self.app_window, "", ("Arial", 35, "bold"), "lightgreen"
        )

    def fill_entries(self):
        self.entry_map["city_var"] = EntryPack(
            self.app_window, self.text_grabber, ("Arial", 30, "bold"), "blue"
        )

    def fill_buttons(self):
        self.button_map["search_button"] = ButtonPack(
            self.app_window,
            "search weather",
            ("Arial", 25, "bold"),
            "while",
            "red",
            self.display_weather,
            20,
        )

    def display_weather(self):
        city_name = self.text_grabber.get()
        weather_report = self.api_data.find_weather_by_city(city_name)
        if weather_report:
            self.label_map["location"].set_by_key(
                "text", "{}, {}".format(weather_report[0], weather_report[1])
            )
            self.label_map["temperature"].set_by_key(
                "text",
                "{} C, {} F".format(weather_report[1], weather_report[2]),
            )
            self.label_map["weather"].set_by_key("text", weather_report[0])
        else:
            messagebox.showerror("error", "city does not exist")
