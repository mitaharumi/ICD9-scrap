from playwright.sync_api import sync_playwright
import json

from robot import Robot


class Main:
    def __init__(self):
        self.browser = p.chromium.launch(chromium_sandbox=False, headless=False)
        self.context = self.browser.new_context(viewport={'width': 1280, 'height': 1024})
        self.page = self.context.new_page()
        self.page.set_default_navigation_timeout(120000)
        self.robot = Robot(self.page)

    def run(self):
        illness = dict(self.robot.illness_mapping(self.robot.url_mapping()))
        with open('illness.json', 'w') as file:
            json.dump(illness, file)

# while True:
with sync_playwright() as p:
    m = Main().run()
