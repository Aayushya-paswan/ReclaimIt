from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.label import Label
from kivy.app import App
from kivy.animation import Animation
from Reclaim_func import styled_button, GradientBackground, AnimatedCard


class HomeScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = GradientBackground()

        self.card = AnimatedCard(orientation='vertical', padding=25, spacing=25,
                                 size_hint=(0.9, 0.72), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.card.opacity = 0  # animate later

        # Headline (added later in on_enter with animation)
        self.headline = Label(
            text='',
            markup=True,
            font_size='30sp',
            size_hint=(1, None),
            height=60,
            halign='center',
            color=(0.1, 0.1, 0.1, 1),
            opacity=0  # animate later
        )

        # Buttons
        self.btns = [
            styled_button('I found a lost item', (0.2, 0.6, 0.8, 1)),
            styled_button('I lost my belonging', (0.2, 0.6, 0.8, 1)),
            styled_button('See Lost Items List', (0.2, 0.6, 0.8, 1)),
            styled_button('See Found Items List', (0.2, 0.6, 0.8, 1)),
            styled_button('Report Campus Issue', (0.8, 0.5, 0.5, 1))
        ]

        transitions = [
            self.go_to_found_form,
            self.go_to_lost_form,
            self.go_to_lost_list,
            self.go_to_found_list,
            self.go_to_report_form
        ]

        for btn, action in zip(self.btns, transitions):
            btn.opacity = 0  # animate each button separately
            btn.bind(on_press=action)
            self.card.add_widget(btn)

        self.layout.add_widget(self.card)
        self.add_widget(self.layout)

    def on_enter(self):
        username = App.get_running_app().username
        self.headline.text = f'[b]Welcome to ReclaimIt, {username}![/b]'
        self.card.clear_widgets()
        self.card.add_widget(self.headline)

        # Add buttons back
        for btn in self.btns:
            self.card.add_widget(btn)

        # Animate the card fade-in
        Animation(opacity=1, d=0.6, t='out_quad').start(self.card)

        # Animate headline
        Animation(opacity=1, font_size=32, d=0.7, t='out_back').start(self.headline)

        # Animate buttons with slight delays
        for i, btn in enumerate(self.btns):
            Animation(opacity=1, d=0.4, t='in_quad').start(btn)

    def go_to_lost_form(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'lost_form'

    def go_to_found_form(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'found_form'

    def go_to_lost_list(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'lost_list'

    def go_to_found_list(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'found_list'

    def go_to_report_form(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'report_form'
