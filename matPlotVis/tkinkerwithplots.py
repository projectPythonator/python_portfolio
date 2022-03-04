from tkinter import Button, Frame, Tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class BarGraphPack:
    def __init__(self):
        self.graph = Figure()

    def fill_graph(self, labs, data, frame):
        ax = self.graph.add_subplot(111)
        ax.pie(
            data,
            radius=1,
            labels=labs,
            autopct="%0.2f%%",
            shadow=True,
        )
        self.pie_chart = FigureCanvasTkAgg(self.graph, frame)
        self.pie_chart.get_tk_widget().pack()


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


class AppWindow:
    def __init__(self, window_title, window_colour, window_size):
        self.app_window = Tk()
        self.app_window.title(window_title)
        self.app_window.configure(bg=window_colour)
        self.app_window.geometry(window_size)
        self.button_map = {}
        self.chart = BarGraphPack()

    def fill_buttons(self):
        self.button_map["plot"] = ButtonPack(
            self.app_window,
            "plot graph",
            ("Arial", 25, "bold"),
            "white",
            "red",
            self.display_plot,
            20,
        )

    def display_plot(self):
        frame = Frame(self.app_window)
        frame.pack()
        self.chart.fill_graph(
            ["AMZN", "AAPL", "JETS", "CCL", "NCLH"],
            [15, 25, 40, 10, 10],
            frame,
        )

    def enter_loop(self):
        self.app_window.mainloop()


def main():
    my_app = AppWindow("plot app", "black", "700x400")
    my_app.fill_buttons()
    my_app.enter_loop()


main()
