""" Powered by @Google
Available Commands:
.google <query>
.google image <query>
.google reverse search"""

import asyncio
import os
from re import findall
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from requests import get
from urllib.parse import quote_plus
from urllib.error import HTTPError
from google_images_download import google_images_download
from gsearch.googlesearch import search
from indus.utils import admin_cmd, sudo_cmd, eor


def progress(current, total):
    logger.info("Downloaded {} of {}\nCompleted {}".format(current, total, (current / total) * 100))


@indus.on(admin_cmd("go (.*)", outgoing=True))
@indus.on(sudo_cmd("go (.*)", allow_sudo=True))
async def _(event):
    ievent = await eor(event,"`Processing... ✍️🙇`")
    match_ = event.pattern_match.group(1)
    match = quote_plus(match_)
    if not match:
        await ievent.edit("`I can't search nothing !!`")
        return
    plain_txt = get(f"https://www.startpage.com/do/search?cmd=process_search&query={match}", 'html').text
    soup = BeautifulSoup(plain_txt, "lxml")
    msg = ""
    for result in soup.find_all('a', {'class': 'w-gl__result-title'}):
        title = result.text
        link = result.get('href')
        msg += f"**{title}**{link}\n"
    await ievent.edit("**Google Search Query:**\n\n`" + match_ + "`\n\n**Results:**\n" + msg)


@indus.on(admin_cmd("gimg (.*)", outgoing=True))
@indus.on(sudo_cmd("gimg (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    ievent = await event.edit("Processing ...")
    input_str = event.pattern_match.group(1)
    response = google_images_download.googleimagesdownload()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    arguments = {
        "keywords": input_str,
        "limit": Config.TG_GLOBAL_ALBUM_LIMIT,
        "format": "jpg",
        "delay": 1,
        "safe_search": True,
        "output_directory": Config.TMP_DOWNLOAD_DIRECTORY
    }
    paths = response.download(arguments)
    lst = paths[input_str]
    await borg.send_file(
        event.chat_id,
        lst,
        caption=input_str,
        reply_to=event.message.id,
        progress_callback=progress
    )
    for each_file in lst:
        os.remove(each_file)
    end = datetime.now()
    ms = (end - start).seconds
    await ievent.edit("searched Google for {} in {} seconds.".format(input_str, ms))
    await asyncio.sleep(5)
    await event.delete()


@indus.on(admin_cmd("grs", outgoing=True))
@indus.on(sudo_cmd("grs", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    BASE_URL = "http://www.google.com"
    OUTPUT_STR = "Reply to an image to do Google Reverse Search"
    if event.reply_to_msg_id:
        ievent = await eor(event,"Pre Processing Media")
        previous_message = await event.get_reply_message()
        previous_message_text = previous_message.message
        if previous_message.media:
            downloaded_file_name = await borg.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY
            )
            SEARCH_URL = "{}/searchbyimage/upload".format(BASE_URL)
            multipart = {
                "encoded_image": (downloaded_file_name, open(downloaded_file_name, "rb")),
                "image_content": ""
            }
            # https://stackoverflow.com/a/28792943/4723940
            google_rs_response = requests.post(SEARCH_URL, files=multipart, allow_redirects=False)
            the_location = google_rs_response.headers.get("Location")
            os.remove(downloaded_file_name)
        else:
            previous_message_text = previous_message.message
            SEARCH_URL = "{}/searchbyimage?image_url={}"
            request_url = SEARCH_URL.format(BASE_URL, previous_message_text)
            google_rs_response = requests.get(request_url, allow_redirects=False)
            the_location = google_rs_response.headers.get("Location")
        await ievent.edit("Found Google Result. Pouring some soup on it!")
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
        }
        response = requests.get(the_location, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        # document.getElementsByClassName("r5a77d"): PRS
        prs_div = soup.find_all("div", {"class": "r5a77d"})[0]
        prs_anchor_element = prs_div.find("a")
        prs_url = BASE_URL + prs_anchor_element.get("href")
        prs_text = prs_anchor_element.text
        # document.getElementById("jHnbRc")
        img_size_div = soup.find(id="jHnbRc")
        img_size = img_size_div.find_all("div")
        end = datetime.now()
        ms = (end - start).seconds
        OUTPUT_STR = """{img_size}
**Possible Related Search**: <a href="{prs_url}">{prs_text}</a>

More Info: Open this <a href="{the_location}">Link</a> in {ms} seconds""".format(**locals())
    await ievent.edit(OUTPUT_STR, parse_mode="HTML")
