from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.label import Label
from kivy.app import App
from Reclaim_func import styled_button, styled_textinput, GradientBackground, AnimatedCard
from auth_logic import  is_email_registered,is_user_registered,generate_otp,send_otp_email,verify_otp,register_user

class SignupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = GradientBackground()

        self.card = AnimatedCard(orientation='vertical', padding=25, spacing=15,
                                 size_hint=(0.85, 0.75), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        logo = Label(text='[b]Sign Up to ReclaimIt[/b]', markup=True, font_size=26, color=(0, 0, 0, 1),
                     size_hint=(1, None), height=40)

        self.email_input = styled_textinput('Email')
        self.username_input = styled_textinput('Username')
        self.password_input = styled_textinput('Create Password', password=True)
        self.otp_input = styled_textinput('Enter OTP')
        self.info_label = Label(text='', color=(1, 0, 0, 1), size_hint=(1, None), height=20)

        send_otp_btn = styled_button('Send OTP', (0.8, 0.8, 1, 1), (0, 0, 0, 1))

        send_otp_btn.bind(on_press=self.send_otp)

        verify_btn = styled_button('Verify & Register', (0.2, 0.5, 0.8, 1))
        verify_btn.bind(on_press=self.verify_and_register)

        switch_btn = styled_button('Already have an account? Sign In', (0.9, 0.9, 0.9, 1), (0, 0, 0, 1))
        switch_btn.bind(on_press=self.switch_to_login)

        for widget in [logo, self.email_input, self.username_input, self.password_input,
                       self.otp_input, self.info_label, send_otp_btn, verify_btn, switch_btn]:
            self.card.add_widget(widget)

        layout.add_widget(self.card)
        self.add_widget(layout)

    def send_otp(self, instance):
        email = self.email_input.text.strip()
        if is_email_registered(self.email_input.text.strip()):
            self.info_label.text = "Email already registered plz login."
            return
        if not email:
            self.info_label.text = 'Email is required to send OTP.'
            return
        otp = generate_otp()
        success = send_otp_email(email, otp)
        self.info_label.text = 'OTP sent to email.' if success else 'Failed to send OTP.'

    def verify_and_register(self, instance):
        email = self.email_input.text.strip()
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        entered_otp = self.otp_input.text.strip()

        if not email or not username or not password or not entered_otp:
            self.info_label.text = 'All fields are required.'
            return

        if is_user_registered(username):
            self.info_label.text = 'Username already exists.'
            return

        verified, message = verify_otp(email, entered_otp)
        if verified:
            register_user(email, username, password)
            self.info_label.text = 'Account created. Please login.'
        else:
            self.info_label.text = message

    def switch_to_login(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'