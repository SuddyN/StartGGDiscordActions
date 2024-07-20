import os
import datetime
import time
import pytz
import requests
import pysmashgg
from pysmashgg.api import run_query

STATE = os.environ["STATE"]
TIMEZONE = os.environ["TIMEZONE"]
GAME_ID = os.environ["GAME_ID"]
SHOW_ONLINE_EVENTS = False
WEBHOOK_URL = os.environ["WEBHOOK_URL"]
STARTGG_TOKEN = os.environ["STARTGG_TOKEN"]
CUSTOM_QUERY = """query TournamentsByState($state: String!, $page: Int!, $videogameId: ID!) {
    tournaments(query: {
        perPage: 32
        page: $page
        filter: {
            past: false
            videogameIds: [
                $videogameId
            ]
            addrState: $state
        }
    }) {
        nodes {
            id
            name
            addrState
            city
            countryCode
            createdAt
            startAt
            endAt
            hasOfflineEvents
            hasOnlineEvents
            images {
                id
                height
                width
                ratio
                type
                url
            }
            isRegistrationOpen
            numAttendees
            primaryContact
            primaryContactType
            registrationClosesAt
            slug
            state
            streams {
                id
                streamName
            }
            timezone
            venueAddress
            venueName
        }
    }
}"""


def tournaments_filter(response, earliestTime: datetime, latestTime: datetime, useCreatedAt: bool):
    if response['data']['tournaments'] is None:
        return

    if response['data']['tournaments']['nodes'] is None:
        return

    tournaments = []

    for node in response['data']['tournaments']['nodes']:
        checkDate = node['startAt']
        if useCreatedAt:
            checkDate = node["createdAt"]
        if checkDate < earliestTime.timestamp():
            continue
        if checkDate > latestTime.timestamp():
            continue

        tournaments.append(node)

    tournaments.sort(key=lambda t: t["startAt"])
    return tournaments


def make_embeds(tournament):
    profile = None
    banner = None
    for image in tournament["images"]:
        if image["type"] == 'profile':
            profile = {"url": image["url"]}
        if image["type"] == 'banner':
            banner = {"url": image["url"]}
    date = datetime.datetime.fromtimestamp(tournament["startAt"], tz=pytz.timezone(TIMEZONE)).strftime('%A, %B %d')
    return [
        {
            "title": tournament["name"],
            "url": f'https://start.gg/{tournament["slug"]}',
            "color": 102204,
            "description": f'{date}\n{tournament["venueAddress"]}\nPrimary Contact: {tournament["primaryContact"]}',
            "thumbnail": profile,
            "image": banner,
            "footer": {"text": "Created by Suddy - LOVE&PEACE"},
        }
    ]


def main():
    """Start the script."""

    tz = pytz.timezone(TIMEZONE)
    this_morning = datetime.datetime.combine(datetime.datetime.now(tz).date(), datetime.time(0, 0, tzinfo=tz), tzinfo=tz)
    tomorrow = this_morning + datetime.timedelta(days=1)
    overmorrow = this_morning + datetime.timedelta(days=2)
    next_week = this_morning + datetime.timedelta(days=8)

    smash = pysmashgg.SmashGG(STARTGG_TOKEN, True)    
    variables = {"state": STATE, "page": 1, "videogameId": GAME_ID}
    response = run_query(CUSTOM_QUERY, variables, smash.header, smash.auto_retry)
    tournaments_tomorrow = tournaments_filter(response, tomorrow, overmorrow, False)
    tournaments_created_recently = tournaments_filter(response, this_morning, tomorrow, True)
    for tournament in tournaments_tomorrow:
        payload = {
            "username": "Events Tomorrow",
            "avatar_url": "https://miro.medium.com/v2/resize:fit:1400/1*YAC3gljr8cMB4ZPyf3CMLA.png",
            "embeds": make_embeds(tournament),
        }
        requests.post(WEBHOOK_URL, json=payload)
    time.sleep(1)
    tournaments_this_week = []
    if this_morning.weekday() == 5:
        tournaments_this_week = tournaments_filter(response, tomorrow, next_week, False)
        for tournament in tournaments_this_week:
            if tournaments_tomorrow.count(tournament) > 0:
                continue
            payload = {
                "username": "Events Later This Week",
                "avatar_url": "https://miro.medium.com/v2/resize:fit:1400/1*YAC3gljr8cMB4ZPyf3CMLA.png",
                "embeds": make_embeds(tournament),
            }
            requests.post(WEBHOOK_URL, json=payload)
    time.sleep(1)
    for tournament in tournaments_created_recently:
        if tournaments_tomorrow.count(tournament) > 0:
            continue
        if tournaments_this_week.count(tournament) > 0:
            continue
        payload = {
            "username": "Events Created Today",
            "avatar_url": "https://miro.medium.com/v2/resize:fit:1400/1*YAC3gljr8cMB4ZPyf3CMLA.png",
            "embeds": make_embeds(tournament),
        }
        requests.post(WEBHOOK_URL, json=payload)


if __name__ == "__main__":
    main()
