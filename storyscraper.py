"""
This module is responsible for scraping stories from a predetermined multireddit.
It imports and filters the json story data and saves the stories in a specified file.
"""

import requests
import json
import os
from unidecode import unidecode
import re

# number of stories to get
n = 20


def scrape_stories() -> dict:
    """
    Scrapes stories from a predetermined multireddit.
    """
    link = f"https://www.reddit.com/r/AmItheAsshole+MaliciousCompliance+nosleep+tifu/.json?count={n}/?sort=top&t=week/"
    data = requests.get(link).json()
    return data


def filter_stories(data: dict) -> list[dict]:
    """
    Filters the stories from the json data.
    :param data:
    :return:
    """
    # TODO: Remove stories that are too short (len)
    # TODO: Remove links from stories (replace entire word with https://, and change it to the word 'link')
    stories = []
    for post in data['data']['children']:
        title = post['data']['title']
        title = filter_text(title)
        text = post['data']['selftext']
        text = filter_text(text)
        stories.append({'title': title, 'text': text})
    return stories


def filter_text(text: str) -> str:
    """
    Filters out any unwanted text from the stories.
    :param text:
    :return:
    """
    text = text.replace('&amp;', 'and')
    text = text.replace('u2026', '...')

    translation_table = str.maketrans({
        ';': '',
        '/': '',
        r'\ '[0]: '',
        '\n': '',
        '\"': '',
        ':': '',
        "'": '',
    })

    text = text.translate(translation_table)

    # Normalize Unicode characters to ASCII
    text = unidecode(text)

    # Remove any remaining unwanted characters using regex
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text


def save_stories(stories: list[dict], file_path: str):
    """
    Saves the stories in a specified file.
    :param stories:
    :param file_path:
    :return:
    """
    if os.path.exists(file_path):
        os.remove(file_path)
    with open(file_path, 'w') as file:
        json.dump(stories, file)


def gather_n_stories(file_path: str = 'temp/stories.json'):
    """
    Main function to scrape stories from a predetermined multireddit.
    :param file_path:
    :return:
    """
    data = scrape_stories()
    stories = filter_stories(data)
    save_stories(stories, file_path)
    return stories


