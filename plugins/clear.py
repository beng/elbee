import operator
import time
from functools import partial

from will.plugin import WillPlugin
from will.decorators import respond_to, hear

NUM_BEFORE_TRUNCATION = 6


def pipe(val, *fns):
    _val = val
    for fn in fns:
        _val = fn(_val)
    return _val


class Clear(WillPlugin):
    def render_reply(self, n):
        content = chr(97 + n) + "\n"
        return content * NUM_BEFORE_TRUNCATION

    def validate_num_times(self, num_times):
        return num_times in range(1, 10)

    def render_num_times(self, num_times):
        if self.validate_num_times(num_times):
            return num_times
        return 4

    def _reply(self, message, num_times):
        for n in range(num_times):
            reply = self.render_reply(n)
            self.reply(message, reply, color="random")
            time.sleep(.15)

    @respond_to("clear (?P<given>\d+)")
    def clear(self, message, given):
        """clear ___ : Sends N replies to clear the screen"""
        pipe(int(given), self.render_num_times, partial(self._reply, message))
        return
