from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout

KV = """
#: import dp kivy.metrics.dp
<RootWidget>:
    orientation: "vertical"
    padding: dp(16)
    spacing: dp(12)

    BoxLayout:
        size_hint_y: None
        height: self.minimum_height
        spacing: dp(8)
        Label:
            text: "BPM:"
            size_hint_x: None
            width: dp(60)
        TextInput:
            id: bpm_input
            text: root.bpm
            input_filter: 'float'
            multiline: False
            on_text_validate: root.convert()
        Spinner:
            id: note_spinner
            text: root.note_label
            values: root.subdivision_labels
            size_hint_x: None
            width: dp(260)

    BoxLayout:
        size_hint_y: None
        height: dp(44)
        spacing: dp(8)
        Button:
            text: "Convert"
            on_release: root.convert()
        Button:
            text: "Clear"
            on_release: root.clear()

    BoxLayout:
        size_hint_y: None
        height: self.minimum_height
        spacing: dp(16)
        Label:
            markup: True
            text: "[b]Milliseconds:[/b]"
            size_hint_x: None
            width: dp(140)
        Label:
            id: ms_label
            text: root.ms_text
            color: 0.1, 0.4, 1, 1
        Label:
            markup: True
            text: "[b]Seconds:[/b]"
            size_hint_x: None
            width: dp(100)
        Label:
            id: s_label
            text: root.s_text
            color: 0.1, 0.6, 0.2, 1

    Label:
        markup: True
        text: "[b]All Subdivisions (1/4 to 1/128)[/b]"
        size_hint_y: None
        height: dp(28)

    ScrollView:
        do_scroll_x: False
        GridLayout:
            id: table_grid
            cols: 3
            size_hint_y: None
            height: self.minimum_height
            row_default_height: dp(30)
            spacing: dp(6)
            # header
            Label:
                markup: True
                text: "[b]Note[/b]"
            Label:
                markup: True
                text: "[b]Milliseconds[/b]"
            Label:
                markup: True
                text: "[b]Seconds[/b]"
"""

class RootWidget(BoxLayout):
    bpm = StringProperty("")
    note_label = StringProperty("Quarter Note (1/4)")
    ms_text = StringProperty("0.00 ms")
    s_text = StringProperty("0.00 s")
    subdivisions_all = ListProperty([
        ("Quarter Note (1/4)", 1.0),
        ("Eighth Note (1/8)", 0.5),
        ("Sixteenth Note (1/16)", 0.25),
        ("Thirty-second Note (1/32)", 0.125),
        ("Sixty-fourth Note (1/64)", 0.0625),
        ("One hundred twenty-eighth Note (1/128)", 0.03125),
    ])
    subdivision_labels = ListProperty([
        "Quarter Note (1/4)",
        "Eighth Note (1/8)",
        "Sixteenth Note (1/16)",
        "Thirty-second Note (1/32)",
        "Sixty-fourth Note (1/64)",
        "One hundred twenty-eighth Note (1/128)",
    ])

    def get_multiplier(self, note):
        multipliers = {
            "Whole Note (1/1)": 4.0,
            "Half Note (1/2)": 2.0,
            "Quarter Note (1/4)": 1.0,
            "Eighth Note (1/8)": 0.5,
            "Sixteenth Note (1/16)": 0.25,
            "Thirty-second Note (1/32)": 0.125,
            "Sixty-fourth Note (1/64)": 0.0625,
            "One hundred twenty-eighth Note (1/128)": 0.03125,
        }
        return multipliers.get(note, 1.0)

    def _validate_bpm(self):
        text = self.ids.bpm_input.text.strip()
        if not text:
            return None
        try:
            value = float(text)
            if value <= 0:
                return None
            return value
        except Exception:
            return None

    def convert(self):
        bpm_value = self._validate_bpm()
        if bpm_value is None:
            # reset
            self.ms_text = "0.00 ms"
            self.s_text = "0.00 s"
            self._render_table(0)
            return
        note = self.ids.note_spinner.text
        mult = self.get_multiplier(note)
        ms_per_quarter = 60000.0 / bpm_value
        milliseconds = ms_per_quarter * mult
        seconds = milliseconds / 1000.0
        self.ms_text = f"{milliseconds:.2f} ms"
        self.s_text = f"{seconds:.3f} s"
        self._render_table(ms_per_quarter)

    def clear(self):
        self.bpm = ""
        self.ids.bpm_input.text = ""
        self.ids.note_spinner.text = "Quarter Note (1/4)"
        self.ms_text = "0.00 ms"
        self.s_text = "0.00 s"
        self._render_table(0)
        self.ids.bpm_input.focus = True

    def _render_table(self, ms_per_quarter):
        grid = self.ids.table_grid
        # remove previous rows while keeping the 3 header widgets
        while len(grid.children) > 3:
            # remove from the end until only headers remain
            grid.remove_widget(grid.children[0])
        # add rows from top to bottom
        for note_name, mult in self.subdivisions_all:
            ms = ms_per_quarter * mult
            sec = ms / 1000.0
            grid.add_widget(App.get_running_app().label_factory(text=note_name))
            grid.add_widget(App.get_running_app().label_factory(text=f"{ms:.2f}"))
            grid.add_widget(App.get_running_app().label_factory(text=f"{sec:.3f}"))

class BPMKivyApp(App):
    def build(self):
        Builder.load_string(KV)
        self.title = "BPM to Milliseconds Converter"
        root = RootWidget()
        root._render_table(0)
        return root

    def label_factory(self, text=""):
        from kivy.uix.label import Label
        return Label(text=text)

if __name__ == "__main__":
    BPMKivyApp().run()
