from apiclient.discovery import build
from will.plugin import WillPlugin
from will.decorators import respond_to, hear


class Mentions(WillPlugin):
    @hear("(ben|pwz)")
    def mention(self, message):
        self.say("@pwzoii", message=message)
