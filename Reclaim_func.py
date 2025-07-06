from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout

def styled_textinput(hint, password=False):
    return TextInput(
        hint_text=hint,
        multiline=False,
        password=password,
        background_normal='',
        background_color=(0.95, 0.95, 1, 1),
        padding=(12, 10),
        font_size=16,
        size_hint=(1, None),
        height=45,
        foreground_color=(0, 0, 0, 1)
    )

class GradientBackground(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.2, 0.6, 0.9, 1)
            Rectangle(pos=self.pos, size=(self.width, self.height * 0.45))
            Color(0.95, 0.95, 1, 1)
            Rectangle(pos=(self.x, self.y + self.height * 0.45), size=(self.width, self.height * 0.55))
class AnimatedCard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity = 0
        with self.canvas.before:
            Color(1, 1, 1, 0.97)
            self.rect = RoundedRectangle(radius=[30], pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
        Animation(opacity=1, d=1.0, t='out_cubic').start(self)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
def styled_textinput(hint, password=False):
    return TextInput(
        hint_text=hint,
        multiline=False,
        password=password,
        background_normal='',
        background_color=(0.95, 0.95, 1, 1),
        padding=(12, 10),
        font_size=16,
        size_hint=(1, None),
        height=45,
        foreground_color=(0, 0, 0, 1)
    )
def styled_button(text, bg_color, text_color=(1, 1, 1, 1)):
    return Button(
        text=text,
        size_hint=(1, None),
        height=45,
        background_normal='',
        background_color=bg_color,
        color=text_color,
        font_size=16
    )
