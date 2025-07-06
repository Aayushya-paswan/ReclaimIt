from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import AsyncImage
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle

import Firebase_config
from Reclaim_func import styled_textinput, styled_button, GradientBackground, AnimatedCard


class FoundFormScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = GradientBackground()

        # Main card
        card = AnimatedCard(orientation='vertical', padding=30, spacing=25,
                            size_hint=(0.9, 0.88), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Title
        title = Label(
            text='[b][color=#1A237E]Report a Found Item[/color][/b]',
            markup=True,
            font_size='26sp',
            size_hint=(1, None),
            height=40,
            halign='center',
            valign='middle',
            color=(0, 0, 0, 1)
        )
        title.bind(size=title.setter('text_size'))

        # Image preview with border
        self.image_preview = AsyncImage(source="", size_hint=(1, None), height=160, allow_stretch=True)
        with self.image_preview.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.rect = RoundedRectangle(radius=[15], pos=self.image_preview.pos, size=self.image_preview.size)
        self.image_preview.bind(pos=lambda *_: setattr(self.rect, 'pos', self.image_preview.pos),
                                size=lambda *_: setattr(self.rect, 'size', self.image_preview.size))

        # Inputs
        self.image_url_input = styled_textinput("Paste image URL here...")
        self.image_url_input.bind(text=self.update_image_preview)

        self.description_input = styled_textinput("Describe the item you found...")
        self.description_input.height = 100
        self.description_input.multiline = True

        # Submit + Back buttons
        submit_btn = styled_button("Submit Found Item", (0.1, 0.6, 0.3, 1))
        submit_btn.bind(on_press=self.submit_found)

        back_btn = styled_button("Back", (0.85, 0.85, 0.85, 1), text_color=(0.1, 0.1, 0.1, 1))
        back_btn.bind(on_press=self.go_back)

        # Add all to card
        for widget in [
            title,
            self.image_preview,
            self.image_url_input,
            self.description_input,
            submit_btn,
            back_btn
        ]:
            card.add_widget(widget)

        layout.add_widget(card)
        self.add_widget(layout)

    def update_image_preview(self, instance, value):
        self.image_preview.source = value

    def submit_found(self, instance):
        image_url = self.image_url_input.text.strip()
        description = self.description_input.text.strip()

        if not image_url or not description:
            self.show_popup("Both image URL and description are required.")
            return

        try:
            email1 = Firebase_config.get_email(App.get_running_app().username)
            Firebase_config.add_found_item(image_url, description, email1)
            self.show_popup("Found item submitted successfully!", success=True)

            # Reset form
            self.image_url_input.text = ""
            self.description_input.text = ""
            self.image_preview.source = ""
        except Exception as e:
            self.show_popup(f"Failed to submit: {str(e)}", success=False)

    def show_popup(self, message, success=False):
        box = BoxLayout(orientation='vertical', padding=15, spacing=15)
        label = Label(
            text=message,
            color=(0.1, 0.6, 0.1, 1) if success else (1, 0.1, 0.1, 1),
            halign='center',
            valign='middle'
        )
        label.bind(size=label.setter('text_size'))
        box.add_widget(label)

        btn = styled_button("OK", (0.75, 0.75, 0.75, 1), text_color=(0, 0, 0, 1))
        btn.bind(on_press=lambda *a: popup.dismiss())
        box.add_widget(btn)

        popup = Popup(title="Message", content=box, size_hint=(0.8, 0.35))
        popup.open()

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'home'
