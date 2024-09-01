# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..utils import (
    ExtractorError,
    int_or_none,
    try_get,
    unified_timestamp,
)

class MiniTVIE(InfoExtractor):
    _VALID_URL = r'https?:\/\/(?:www\.)?amazon\.in\/minitv\/tp\/+(?P<id>[a-z0-9-]+)'
    _GEO_COUNTRIES = ['IN']
    _TESTS = [{
        'url': 'https://www.amazon.in/minitv/tp/2cd75fd8-0278-41ab-bb30-45bceeddfb1e',
        'info_dict': {
            'id': '0_8ledb18o',
            'ext': 'mp4',
            'title': 'Ishq Ka Rang Safed - Season 01 - Episode 340',
            'description': 'md5:06291fbbbc4dcbe21235c40c262507c1',
            'timestamp': 1472162937,
            'upload_date': '20160825',
            'duration': 1146,
            'series': 'Ishq Ka Rang Safed',
            'season_number': 1,
            'episode': 'Is this the end of Kamini?',
            'episode_number': 340,
            'view_count': int,
            'like_count': int,
        },
        'params': {
            'skip_download': True,
        },
        'expected_warnings': ['Failed to download m3u8 information'],
    }, {
        'url': 'https://www.amazon.in/minitv/tp/38f200a1-953a-414c-955a-cd21d9aba047',
        'only_matching': True,
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)

        webpage = self._download_webpage(url, video_id)

        jsonText = self._html_search_regex("\<script id\=\"\_\_NEXT\_DATA\_\_\" type\=\"application\/json\" crossorigin\=\"anonymous\"\>(.*?)\<\/script\>", webpage, "json")

        webdata = self._parse_json(jsonText, video_id)['props']['pageProps']['ssrProps']

        if 'metaData' not in webdata:
            raise ExtractorError("Content Not Available", expected=True)
        
        metaData = webdata['metaData']
        media = metaData['contentDetails']

        manifestUrl = webdata['widgets'][0]['data']['playbackAssets']['manifestURL']

        title = media['name']
        formats, subtitles = self._extract_mpd_formats_and_subtitles(manifestUrl, video_id, mpd_id='dash')
        self._sort_formats(formats)

        series, season, season_number, episode, episode_number = [None] * 5

        if media['vodType'] == "EPISODE":
            series = media['seriesName']
            season = media['seasonName']
            season_number = media['seasonNumber']
            episode_number = media['episodeNumber']
            episode = title

        return {
            'id': video_id,
            'title': title,
            'thumbnail': media['imageSrc'],
            'description': media['synopsis'],
            'series': series,
            'season': season,
            'season_number': season_number,
            'episode': episode,
            'episode_number': episode_number,
            'webpage_url': metaData['canonicalUrl'],
            'duration': int_or_none(media['contentLengthInSeconds']),
            'formats': formats,
            'subtitles': subtitles if subtitles else None,
        }
