from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class RecorderTest(BaseCase):
    def test_recording(self):
        self.open("file:///Users/jwr003/coding/pytest-tui/html_report.html")
