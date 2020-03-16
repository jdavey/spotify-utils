import requests
from bs4 import BeautifulSoup
import logging
import sys

from dateutil.parser import parse

EPISODE_URL = "https://www.bbc.co.uk/programmes/b03hjfww/episodes/player"

logger = logging.getLogger(__name__)


def parse_program_id(link):
    return link.split("/")[-1]


def get_program_player_url(program_id):
    return "https://www.bbc.co.uk/sounds/play/%s" % program_id

def get_program_url(program_id):
    return "https://www.bbc.co.uk/programmes/%s" % program_id


def _parse_track_from_span(track_span):
    details = track_span.contents
    if len(details) > 4:
        artist = details[1].find("span").contents
        title = details[3].find("span").contents
        return f"{artist[0]} - {title[0]}"

    return None



def fetch_playlist_from_program(program_id):
    program_url = get_program_url(program_id)
    logger.info("Program URL: %s" % program_url)
    player_page_response = requests.get(program_url)
    if player_page_response.status_code != 200:
        logger.error("Unable to read URL %s response: %d" % (EPISODE_URL, player_page_response.status_code))
        sys.exit(1)

    player_soup = BeautifulSoup(player_page_response.content)
    tracks = player_soup.find_all("div", "segment__track")
    program_info = player_soup.find_all("div", "broadcast-event__time beta")

    if program_info:
        program_date = program_info[0].attrs.get('content', "")
        if program_date:
            dt = parse(program_date)
            program_name = f"taggart minus taggart {dt.month}/{dt.day}/{dt.year}"

    return program_name, list(filter(lambda details: details, map(lambda track: _parse_track_from_span(track), tracks)))


def fetch_program_names():
    response = requests.get(EPISODE_URL)
    if response.status_code != 200:
        logger.error("Unable to read URL %s response: %d" % (EPISODE_URL, response.status_code))
        sys.exit(1)

    soup = BeautifulSoup(response.content)
    program_names = list(
        map(lambda link: parse_program_id(link.attrs['href']), soup.find_all("a", "br-blocklink__link")))
    return program_names
