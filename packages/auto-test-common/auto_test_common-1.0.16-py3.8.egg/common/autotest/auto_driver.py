from common.autotest.base_requests import BaseRequest
from playwright.sync_api import Page

class AutoDriver(BaseRequest,Page):

    def get_ui(self, url):
        self.request.get(url)

    def del_ui(self, url):
        self.request.delete(url)
