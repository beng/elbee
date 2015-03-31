from mock import MagicMock, patch
from nose.tools import eq_, ok_

from plugins.youtube import YoutubeSearchPlugin


class TestYoutubePlugin(object):
    def setup(self):
        self.plugin = YoutubeSearchPlugin()

    @patch('will.plugin.WillPlugin.reply')
    @patch('requests.get')
    def test_get_youtube_video_failure(self, mock_get, mock_reply):
        pass
