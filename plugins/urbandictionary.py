import requests
from bs4 import BeautifulSoup
from will.plugin import WillPlugin
from will.decorators import respond_to, hear

class UrbanDictionaryPlugin(WillPlugin):
    @property
    def urban_url(self):
        return "http://www.urbandictionary.com/define.php"

    def _request(self, params=None, timeout=None):
        resp = requests.get(self.urban_url, params=params, timeout=timeout)
        resp.raise_for_status()
        return resp

    def extract_content(self, term):
        resp = self._request(params=dict(term=term))
        html = BeautifulSoup(resp.content)
        top_entry = html.find('div', {'class': 'def-panel'})
        if not top_entry:
            return

        # TODO (bg) - these will prob break. need to set a default val
        definition = top_entry.find('div', {'class': 'meaning'}).text
        example = top_entry.find('div', {'class': 'example'}).text
        return definition, example

    def render_message(self, content):
        return "".join(content)

    @respond_to("(urbandictionary|ud|urban) me (?P<term>.*)$")
    def search(self, message, term):
        """(urbandictionary|ud|urban) me ___ : Search urbandictionary for ___,
        and post the top definition along with the example(s)
        """
        ud_content = self.extract_content(term)
        if ud_content:
            self.reply(message, self.render_message(ud_content))
            return
        self.reply(message, "No entry found for: {}".format(term))
