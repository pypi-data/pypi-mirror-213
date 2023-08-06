import asyncio
import logging
import re

from ripandtear.extractors.common import Common
from ripandtear.utils.custom_types import UrlDictionary
from ripandtear.utils.tracker import Tracker

log = logging.getLogger(__name__)

# Errors
# 'https://i.imgur.com/LKvqXWE.gifv'

prefix = 'imgur'

imgur_re_direct_image = re.compile(
    r"(https?://)([im]\.|www\.)?(imgur\.(com|io))/(\w+)(\.jpg|jpeg|png|gifv|mp4|gif)?")
# 'https://i.imgur.com/I7i8u6b.gifv'
# 'https://i.imgur.com/hCOoORb.png'

imgur_re_album = re.compile(
    r"(https?://)?(([im]\.)|(www.))?(imgur\.(com|io))/((a))/(\w+)")
# 'https://imgur.com/a/1GXfC'
# 'https://imgur.com/a/1GXfC/all'

imgur_re_gallery = re.compile(
    r"(https?://)(imgur\.(com|io))/gallery/(\w+)")
# 'https://imgur.com/gallery/mPIxZnC'

headers = {
    "Authorization": "Client-ID 546c25a59c58ad7"
}


class Imgur(Common):

    def __init__(self):

        self.tracker = Tracker.getInstance()

    def imgur_direct_image_hash(self, url: str) -> str:
        log.debug("Looking for direct image hash")
        direct_image_hash = imgur_re_direct_image.search(url).group(5)
        return direct_image_hash

    async def run(self, url_dictionary: UrlDictionary) -> None:

        if imgur_re_direct_image.match(url_dictionary['url']):

            log.debug("Direct image found. Sending to single download")
            await self.imgur_single_download(self.imgur_direct_image_hash(url_dictionary['url']),
                                             url_dictionary.copy())

        else:
            log.info(f"No regex found for {url_dictionary['url']}")

    async def imgur_single_download(self, image_hash: str, url_dictionary: UrlDictionary) -> None:

        try:
            url_dictionary['prefix'] = prefix
            url_dictionary['headers'] = {
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
            url_dictionary['url_to_download'] = url_dictionary['url']

            if 'gifv' in url_dictionary['url_to_download']:
                url_dictionary['url_to_download'] = url_dictionary['url_to_download'].replace(
                    'gifv', 'mp4')

            url_dictionary['name'] = image_hash
            url_dictionary['extension'] = self.common_find_url_extension(
                url_dictionary['url_to_download'])
            url_dictionary['filename'] = self.common_filename_creator(
                url_dictionary.copy())

            log.info("Url dictionary built. Sending to tracker")
            await self.tracker.add_url_dictionary(url_dictionary.copy())

        except Exception:
            log.error(
                f"Problem downloading image: {url_dictionary['url_to_download']}")
