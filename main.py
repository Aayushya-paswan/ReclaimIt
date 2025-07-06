
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window


Window.clearcolor = (1, 1, 1, 1)
from screens.homescreen import HomeScreen
from screens.signupscreen import SignupScreen
from screens.lostformscreen import LostFormScreen
from screens.lostlistscreen import LostlistScreen
from screens.foundformscreen import FoundFormScreen
from screens.foundlistscreen import FoundlistScreen
from screens.loginscreen import LoginScreen
from screens.reportformscreen import ReportFormScreen


class CampusApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username = ""
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(FoundFormScreen(name='found_form'))
        sm.add_widget(LostFormScreen(name='lost_form'))
        sm.add_widget(LostlistScreen(name='lost_list'))
        sm.add_widget(FoundlistScreen(name='found_list'))
        sm.add_widget(ReportFormScreen(name='report_form'))
        return sm


if __name__ == '__main__':
    CampusApp().run()
