from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.label import Label
from kivy.app import App
from auth_logic import get_user_password
from Reclaim_func import styled_textinput, styled_button, GradientBackground, AnimatedCard

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = GradientBackground()

        self.card = AnimatedCard(orientation='vertical', padding=25, spacing=15,
                                 size_hint=(0.85, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        logo = Label(text='[b]ReclaimIt Login[/b]', markup=True, font_size=28, color=(0, 0, 0, 1), size_hint=(1, None),
                     height=40)

        self.username_input = styled_textinput('Username')
        self.password_input = styled_textinput('Password', password=True)
        self.info_label = Label(text='', color=(1, 0, 0, 1), size_hint=(1, None), height=20)

        login_btn = styled_button('Login', (0.2, 0.5, 0.8, 1))
        login_btn.bind(on_press=self.login)

        switch_btn = styled_button("Don't have an account? Sign Up", (0.85, 0.85, 0.85, 1), (0, 0, 0, 1))
        switch_btn.bind(on_press=self.switch_to_signup)

        for widget in [logo, self.username_input, self.password_input, self.info_label, login_btn, switch_btn]:
            self.card.add_widget(widget)

        layout.add_widget(self.card)
        self.add_widget(layout)

    def login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        stored_password = get_user_password(username)
        if stored_password and stored_password == password:
            self.manager.transition = SlideTransition(direction="left")
            App.get_running_app().username = username
            self.manager.current = 'home'
        else:
            self.info_label.text = 'Invalid username or password.'

    def switch_to_signup(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'signup'

