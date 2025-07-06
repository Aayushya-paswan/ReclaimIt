from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle

from Reclaim_func import styled_button, GradientBackground
import Firebase_config

class ReportFormScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # --- Main vertical layout ---
        self.main_layout = BoxLayout(orientation='vertical')

        # --- Top bar with headline + report button ---
        top_bar = BoxLayout(size_hint=(1, None), height=60, padding=10, spacing=10)

        headline = Label(
            text='[b][color=#2E3A59] Anonymous Issues[/color][/b]',
            markup=True,
            font_size='24sp',
            halign='left',
            valign='middle',
            size_hint=(0.7, 1)
        )
        headline.bind(size=headline.setter('text_size'))

        report_btn = styled_button("➕ Report Issue", (0.2, 0.6, 1, 1))
        report_btn.size_hint = (0.3, 1)
        report_btn.bind(on_press=self.open_report_popup)

        top_bar.add_widget(headline)
        top_bar.add_widget(report_btn)

        # --- Scrollable issues container ---
        self.scroll = ScrollView(size_hint=(1, 0.85))
        self.container = GridLayout(cols=1, spacing=15, padding=15, size_hint_y=None)
        self.container.bind(minimum_height=self.container.setter('height'))
        self.scroll.add_widget(self.container)

        # --- Back Button ---
        back_btn = styled_button("← Back", (0.9, 0.9, 0.9, 1), text_color=(0, 0, 0, 1))
        back_btn.size_hint = (0.3, None)
        back_btn.height = 50
        back_btn.pos_hint = {'center_x': 0.5}
        back_btn.bind(on_press=self.go_back)

        # Add everything to main_layout
        self.main_layout.add_widget(top_bar)
        self.main_layout.add_widget(self.scroll)
        self.main_layout.add_widget(back_btn)

        # Use a background
        self.bg_layout = GradientBackground()
        self.bg_layout.add_widget(self.main_layout)
        self.add_widget(self.bg_layout)

    def on_enter(self):
        self.container.clear_widgets()
        issues = Firebase_config.get_all_anonymous_issues()
        print("📄 Retrieved issues from DB:", issues)  # <-- Add this line

        if issues:
            for issue_id, data in issues.items():
                print("➡️ Card:", issue_id, data)
                card = self.create_issue_card(data.get("issue", ""))
                self.container.add_widget(card)
        else:
            self.container.add_widget(Label(
                text="[b][color=#777777]No issues reported yet.[/color][/b]",
                markup=True,
                font_size=18,
                halign='center',
                size_hint_y=None,
                height=100
            ))

    def create_issue_card(self, issue_text):
        card = BoxLayout(orientation='vertical', padding=15, spacing=10,
                         size_hint=(1, None), height=120)

        with card.canvas.before:
            Color(1, 1, 1, 0.95)
            rect = RoundedRectangle(radius=[15], pos=card.pos, size=card.size)
            card.bind(pos=lambda *_: setattr(rect, 'pos', card.pos),
                      size=lambda *_: setattr(rect, 'size', card.size))

        label = Label(
            text=f"[b]{issue_text}[/b]",
            markup=True,
            font_size='16sp',
            size_hint=(1, None),
            height=80,
            halign='left',
            valign='top',
            color=(0, 0, 0, 1)  # 🟢 Black color for text
        )
        label.bind(size=label.setter('text_size'))
        card.add_widget(label)
        return card

    def open_report_popup(self, instance):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        input_box = TextInput(
            hint_text="Describe the issue anonymously...",
            multiline=True,
            size_hint=(1, None),
            height=120
        )

        submit_btn = Button(
            text="Submit",
            size_hint=(1, None),
            height=45,
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )

        layout.add_widget(input_box)
        layout.add_widget(submit_btn)

        popup = Popup(title="📣 Report Anonymous Issue", content=layout, size_hint=(0.85, 0.5))

        def submit_issue(instance):
            issue = input_box.text.strip()
            if issue:
                Firebase_config.report_anonymous_issue(issue)
                popup.dismiss()

                success_popup = Popup(
                    title="✅ Submitted",
                    content=Label(text="Your issue has been submitted anonymously."),
                    size_hint=(0.75, 0.3)
                )
                success_popup.open()
                self.on_enter()

        submit_btn.bind(on_press=submit_issue)
        popup.open()

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'home'
