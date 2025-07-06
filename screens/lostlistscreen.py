from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.graphics import Color, RoundedRectangle

from Reclaim_func import styled_button, GradientBackground
import Firebase_config


class LostlistScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GradientBackground()

        # --- Stylish Headline ---
        headline = Label(
            text='[b][color=#222222]📋 List of Lost Items[/color][/b]',
            markup=True,
            font_size='28sp',
            size_hint=(1, None),
            height=70,
            halign='center',
            valign='middle'
        )
        headline.bind(size=headline.setter('text_size'))
        self.layout.add_widget(headline)

        # --- Scrollable Lost Items Container ---
        self.scroll = ScrollView(size_hint=(1, 0.85), pos_hint={'center_x': 0.5})
        self.container = GridLayout(cols=1, spacing=20, padding=20, size_hint_y=None)
        self.container.bind(minimum_height=self.container.setter('height'))
        self.scroll.add_widget(self.container)

        # --- Back Button ---
        back_btn = styled_button("← Back", (0.9, 0.9, 0.9, 1), text_color=(0, 0, 0, 1))
        back_btn.size_hint = (0.3, None)
        back_btn.height = 50
        back_btn.pos_hint = {'center_x': 0.5}
        back_btn.bind(on_press=self.go_back)

        self.layout.add_widget(self.scroll)
        self.layout.add_widget(back_btn)
        self.add_widget(self.layout)

    def on_enter(self):
        self.container.clear_widgets()
        lost_items = Firebase_config.get_all_lost_items()
        if lost_items:
            for item_id, item_data in lost_items.items():
                self.container.add_widget(self.create_lost_card(item_id, item_data))
        else:
            self.container.add_widget(Label(
                text="[b][color=#888888]No lost items reported yet.[/color][/b]",
                markup=True,
                font_size=18,
                halign='center',
                size_hint_y=None,
                height=100
            ))

    def create_lost_card(self, item_id, item_data):
        card = BoxLayout(orientation='vertical', spacing=10, padding=15,
                         size_hint=(1, None), height=350)

        with card.canvas.before:
            Color(1, 1, 1, 0.95)
            rect = RoundedRectangle(radius=[20], pos=card.pos, size=card.size)
            card.bind(pos=lambda *_: setattr(rect, 'pos', card.pos),
                      size=lambda *_: setattr(rect, 'size', card.size))

        # --- Email Display ---

        email_label = Label(
            text=f"[b][color=#555555]Posted by: {item_data.get('posted_by', 'N/A')}",
            markup=True,
            size_hint=(1, 0.1),
            font_size='14sp',
            halign='center',
            valign='middle'
        )
        ee = item_data.get('posted_by', 'N/A')
        email_label.bind(size=email_label.setter('text_size'))

        # --- Image ---
        image_url = item_data.get("image", "No Image")
        image = AsyncImage(source=image_url, size_hint=(1, 0.55), allow_stretch=True)

        # --- Description ---
        desc = Label(
            text=f"[b][color=#D32F2F]{item_data.get('description', 'No Description')}[/color][/b]",
            markup=True,
            size_hint=(1, 0.15),
            font_size='16sp',
            halign='center',
            valign='middle'
        )
        desc.bind(size=desc.setter('text_size'))

        # --- Status ---
        status_text = item_data.get('status', 'Unknown')
        status = Label(
            text=f"[b]Status:[/b] {status_text}",
            markup=True,
            size_hint=(1, 0.1),
            font_size='14sp',
            color=(0.2, 0.6, 0.2, 1)
        )

        # --- Found Button ---
        found_btn = Button(
            text="✅ Click if you found it",
            background_color=(0.2, 0.7, 0.4, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, 0.15),
            bold=True
        )
        found_btn.bind(on_press=lambda instance: self.go_to_found_form(item_id))

        # --- Add all widgets to card ---
        for widget in [email_label, image, desc, status, found_btn]:
            card.add_widget(widget)

        return card

    def go_to_found_form(self, item_id):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'found_form'

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'home'
