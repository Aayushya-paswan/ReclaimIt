from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.app import App

from Reclaim_func import styled_textinput, styled_button, GradientBackground, AnimatedCard
import Firebase_config


class LostFormScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = GradientBackground()

        card = AnimatedCard(orientation='vertical', padding=25, spacing=20,
                            size_hint=(0.9, 0.85), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        title = Label(text='[b]Report a Lost Item[/b]', markup=True, font_size=24,
                      size_hint=(1, None), height=40, color=(0, 0, 0, 1))

        self.image_url_input = styled_textinput("Paste image URL here...")
        self.image_url_input.multiline = False
        self.image_url_input.bind(text=self.update_image_preview)

        self.image_preview = AsyncImage(source="", size_hint=(1, None), height=150, allow_stretch=True)

        self.description_input = styled_textinput("Describe your lost item...")
        self.description_input.height = 100
        self.description_input.multiline = True

        submit_btn = styled_button("🚨 Report Lost Item", (1, 0.3, 0.3, 1))
        submit_btn.bind(on_press=self.submit_lost)

        back_btn = styled_button("← Back", (0.8, 0.8, 0.8, 1), text_color=(0, 0, 0, 1))
        back_btn.bind(on_press=self.go_back)

        for widget in [title, self.image_url_input, self.image_preview,
                       self.description_input, submit_btn, back_btn]:
            card.add_widget(widget)

        layout.add_widget(card)
        self.add_widget(layout)

    def update_image_preview(self, instance, value):
        url = value.strip()
        if url.startswith("http"):
            self.image_preview.source = url
        else:
            self.image_preview.source = ""

    def show_popup(self, title, message, color=(0, 0, 0, 1)):
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        content.add_widget(Label(text=message, color=color, font_size=16))
        close_btn = styled_button("OK", (0.6, 0.8, 1, 1))
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.4), auto_dismiss=True)
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        popup.open()

    def submit_lost(self, instance):
        description = self.description_input.text.strip()
        image_url = self.image_url_input.text.strip()

        if not description:
            self.show_popup("Error", "Description is required.")
            return

        try:
            email1 = Firebase_config.get_email(App.get_running_app().username)
            Firebase_config.add_lost_item(image_url, description, email1)
            self.show_popup("Success", "Your lost item report has been submitted!")
            self.description_input.text = ""
            self.image_url_input.text = ""
            self.image_preview.source = ""
        except Exception as e:
            self.show_popup("Error", f" Failed to save to database:\n{str(e)}")

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'home'
