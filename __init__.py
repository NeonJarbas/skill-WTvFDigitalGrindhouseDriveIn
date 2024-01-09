import random
from os.path import join, dirname

import requests
from json_database import JsonStorageXDG

from ovos_utils.ocp import MediaType, PlaybackType
from ovos_workshop.decorators.ocp import ocp_search, ocp_featured_media
from ovos_workshop.skills.common_play import OVOSCommonPlaybackSkill


class WTvFDigitalGrindhouseDriveInSkill(OVOSCommonPlaybackSkill):
    def __init__(self, *args, **kwargs):
        self.supported_media = [MediaType.MOVIE]
        self.skill_icon = join(dirname(__file__), "res", "logo.jpg")
        self.default_bg = self.skill_icon
        self.archive = JsonStorageXDG("WTvFDigitalGrindhouseDriveIn", subfolder="OCP")
        super().__init__(*args, **kwargs)

    def initialize(self):
        self._sync_db()
        self.load_ocp_keywords()

    def load_ocp_keywords(self):
        titles = []
        genre = ["horror movie","slasher", "exploitation",
                 "grindhouse","classic movie", "science fiction"]

        for url, data in self.archive.items():
            t = data["title"]
            title, year = t.split("(")
            year = year.split(")")[0]
            titles.append(title.strip())

        self.register_ocp_keyword(MediaType.MOVIE,
                                  "movie_name", titles)
        self.register_ocp_keyword(MediaType.MOVIE,
                                  "film_genre", genre)
        self.register_ocp_keyword(MediaType.MOVIE,
                                  "movie_streaming_provider",
                                  ["WTvFDigitalGrindhouseDriveIn", "WTvF",
                                   "Digital Grindhouse", "Grindhouse DriveIn"])

    def _sync_db(self):
        bootstrap = "https://github.com/JarbasSkills/skill-WTvFDigitalGrindhouseDriveIn/raw/dev/bootstrap.json"
        data = requests.get(bootstrap).json()
        self.archive.merge(data)
        self.schedule_event(self._sync_db, random.randint(3600, 24 * 3600))

    def get_playlist(self, score=50, num_entries=25):
        return {
            "match_confidence": score,
            "media_type": MediaType.MOVIE,
            "playlist": self.featured_media()[:num_entries],
            "playback": PlaybackType.VIDEO,
            "skill_icon": self.skill_icon,
            "image": self.skill_icon,
            "bg_image": self.default_bg,
            "title": "WTvF Digital Grindhouse Drive In (Movie Playlist)",
            "author": "WTvF Digital Grindhouse Drive In"
        }

    @ocp_search()
    def search_db(self, phrase, media_type):
        base_score = 15 if media_type == MediaType.MOVIE else 0
        entities = self.ocp_voc_match(phrase)

        title = entities.get("movie_name")
        skill = "movie_streaming_provider" in entities  # skill matched

        base_score += 30 * len(entities)

        if title:
            candidates = [video for video in self.archive.values()
                          if title.lower() in video["title"].lower()]
            for video in candidates:
                yield {
                    "title": video["title"],
                    "author": video["author"],
                    "match_confidence": min(100, base_score),
                    "media_type": MediaType.MOVIE,
                    "uri": "youtube//" + video["url"],
                    "playback": PlaybackType.VIDEO,
                    "skill_icon": self.skill_icon,
                    "skill_id": self.skill_id,
                    "image": video["thumbnail"],
                    "bg_image": self.default_bg
                }

        if skill:
            yield self.get_playlist()

    @ocp_featured_media()
    def featured_media(self):
        return [{
            "title": video["title"],
            "image": video["thumbnail"],
            "match_confidence": 70,
            "media_type": MediaType.MOVIE,
            "uri": "youtube//" + video["url"],
            "playback": PlaybackType.VIDEO,
            "skill_icon": self.skill_icon,
            "bg_image": video["thumbnail"],
            "skill_id": self.skill_id
        } for video in self.archive.values()]


if __name__ == "__main__":
    from ovos_utils.messagebus import FakeBus

    s = WTvFDigitalGrindhouseDriveInSkill(bus=FakeBus(), skill_id="t.fake")
    for r in s.search_db("Plan 9 from Outer Space", MediaType.MOVIE):
        print(r)
        # {'title': 'Plan 9 from Outer Space (1959) *public domain', 'author': 'WTvF! - Digital Grindhouse & Drive-In', 'match_confidence': 45, 'media_type': <MediaType.MOVIE: 10>, 'uri': 'youtube//https://youtube.com/watch?v=4z6VLR2GA1w', 'playback': <PlaybackType.VIDEO: 1>, 'skill_icon': 'https://github.com/OpenVoiceOS/ovos-ocp-audio-plugin/raw/master/ovos_plugin_common_play/ocp/res/ui/images/ocp.png', 'skill_id': 't.fake', 'image': 'https://i.ytimg.com/vi/4z6VLR2GA1w/sddefault.jpg', 'bg_image': '/home/miro/PycharmProjects/OCP_sprint/skills/skill-WTvFDigitalGrindhouseDriveIn/res/logo.jpg'}
