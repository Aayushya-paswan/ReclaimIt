from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.image import AsyncImage
from kivy.graphics import Color, RoundedRectangle
from kivy.app import App
from kivy.animation import Animation

from Reclaim_func import styled_button, GradientBackground
import Firebase_config


class FoundlistScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GradientBackground()

        headline = Label(
            text='[b][color=#1E3A5F]Items Found on Campus[/color][/b]',
            markup=True,
            font_size='28sp',
            size_hint=(1, None),
            height=70,
            halign='center',
            valign='middle'
        )
        headline.bind(size=headline.setter('text_size'))
        self.layout.add_widget(headline)

        # Scrollable card area
        self.scroll = ScrollView(size_hint=(1, 0.85), pos_hint={'center_x': 0.5})
        self.container = GridLayout(cols=1, spacing=20, padding=30, size_hint_y=None)
        self.container.bind(minimum_height=self.container.setter('height'))
        self.scroll.add_widget(self.container)

        back_btn = styled_button("← Back", (0.9, 0.9, 0.9, 1), text_color=(0, 0, 0, 1))
        back_btn.size_hint = (0.35, None)
        back_btn.height = 50
        back_btn.pos_hint = {'center_x': 0.5}
        back_btn.bind(on_press=self.go_back)

        self.layout.add_widget(self.scroll)
        self.layout.add_widget(back_btn)
        self.add_widget(self.layout)

    def on_enter(self):
        self.container.clear_widgets()
        found_items = Firebase_config.get_all_found_items()

        if found_items:
            for item_id, item_data in found_items.items():
                card = self.create_found_card(item_id, item_data)
                self.container.add_widget(card)
                Animation(opacity=1, d=0.3, t='out_quad').start(card)
        else:
            self.container.add_widget(Label(
                text="[b][color=#777777]No items have been reported yet.[/color][/b]",
                markup=True,
                font_size=18,
                halign='center',
                size_hint_y=None,
                height=100
            ))

    def create_found_card(self, item_id, item_data):
        card = BoxLayout(orientation='vertical', spacing=12, padding=15,
                         size_hint=(1, None), height=400, opacity=0)

        with card.canvas.before:
            Color(1, 1, 1, 0.94)
            rect = RoundedRectangle(radius=[25], pos=card.pos, size=card.size)
            card.bind(pos=lambda *_: setattr(rect, 'pos', card.pos),
                      size=lambda *_: setattr(rect, 'size', card.size))

        posted_by = item_data.get("posted_by", "Unknown")
        status_text = item_data.get('status', 'unknown').capitalize()

        image_url = item_data.get("image", "")
        image = AsyncImage(source=image_url, size_hint=(1, 0.55), allow_stretch=True, keep_ratio=True)

        email_label = Label(
            text=f"📨 [b]Posted by:[/b] {posted_by}",
            markup=True,
            font_size='14sp',
            size_hint=(1, 0.1),
            color=(0.1, 0.3, 0.6, 1)
        )

        desc = Label(
            text=f"[b][color=#D84315]{item_data.get('description', 'No Description')}[/color][/b]",
            markup=True,
            font_size='16sp',
            size_hint=(1, 0.15),
            halign='center',
            valign='middle'
        )
        desc.bind(size=desc.setter('text_size'))

        # Status styling
        status_color = (0.2, 0.6, 0.2, 1) if "claimed" not in status_text.lower() else (0.6, 0.3, 0.2, 1)
        status = Label(
            text=f"📌 [b]Status:[/b] {status_text}",
            markup=True,
            font_size='14sp',
            size_hint=(1, 0.1),
            color=status_color
        )

        card.add_widget(image)
        card.add_widget(desc)
        card.add_widget(email_label)
        card.add_widget(status)

        if status_text.lower() != "claimed":
            claim_btn = Button(
                text="🎯 Claim This Item",
                background_color=(0.2, 0.6, 1, 1),
                color=(1, 1, 1, 1),
                size_hint=(1, 0.15),
                bold=True
            )
            claim_btn.bind(on_press=lambda instance: self.ask_verification(item_id, posted_by))
            card.add_widget(claim_btn)

        return card

    def ask_verification(self, item_id, recipient_email):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        instruction = Label(text="Describe the item to verify:", size_hint=(1, None), height=40)
        self.verification_input = TextInput(hint_text="Enter unique detail...", multiline=False, size_hint=(1, None), height=40)
        submit_btn = Button(text="Submit", size_hint=(1, None), height=45, background_color=(0.3, 0.6, 1, 1))

        layout.add_widget(instruction)
        layout.add_widget(self.verification_input)
        layout.add_widget(submit_btn)

        popup = Popup(title="Verification Required", content=layout, size_hint=(0.85, 0.4))

        def submit_verification(instance):
            answer = self.verification_input.text.strip()
            if not answer:
                return
            try:
                email1 = Firebase_config.get_email(App.get_running_app().username)
                Firebase_config.send_claim_verification_email(recipient_email, answer, email1)
                Firebase_config.update_found_item_status(item_id, "claimed")
                popup.dismiss()

                Popup(
                    title="Email Sent",
                    content=Label(text="Verification email has been sent to the one who has found it"),
                    size_hint=(0.75, 0.3)
                ).open()

                self.on_enter()

            except Exception as e:
                Popup(
                    title="Error",
                    content=Label(text=f"Failed to send email: {str(e)}"),
                    size_hint=(0.75, 0.3)
                ).open()

        submit_btn.bind(on_press=submit_verification)
        popup.open()

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'home'
