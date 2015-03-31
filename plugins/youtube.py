import os
import random

from apiclient.discovery import build
from will.plugin import WillPlugin
from will.decorators import respond_to, hear

DEVELOPER_KEY = os.getenv('YOUTUBE_DEV_KEY')
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(query, max_results=50):
    def extract_video_id(result):
        if result['id']['kind'] == 'youtube#video':
            return result['id']['videoId']

    def build_url(video_id):
        if video_id:
            return "https://www.youtube.com/watch?v=" + video_id

    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY
    )
    resp = youtube.search().list(
        q=query,
        part="id, snippet",
        maxResults=max_results
    ).execute()

    video_ids = map(extract_video_id, resp.get('items', []))
    return filter(None, map(build_url, video_ids))

class YoutubeSearchPlugin(WillPlugin):
    def render_url(self, urls):
        return random.choice(urls)

    @respond_to("youtube me (?P<query>.*)$")
    def search(self, message, query):
        """youtube me ___ : Search youtube for ___, and posts a random one"""
        video_urls = youtube_search(query)
        if video_urls:
            self.reply(message, self.render_url(video_urls))
            return
        self.reply(message, "Could not find video for query: `{}`".format(query))
