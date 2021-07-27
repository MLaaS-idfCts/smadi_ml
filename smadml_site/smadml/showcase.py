import asyncio
import json
import os
from http import HTTPStatus

import requests
from pyppeteer import launch

USERNAME = os.environ.get('username')
PASSWORD = os.environ.get('password')
URL = os.environ.get('url')
HEADERS_GET_STATUS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "access-control-allow-origin": "*",
    "crossdomain": "true",
    "pragma": "no-cache",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\"",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin"
    }
HEADERS_SEND_REPORT = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "access-control-allow-origin": "*",
    "content-type": "application/json;charset=UTF-8",
    "crossdomain": "true",
    "pragma": "no-cache"}

DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'user-data-dir')


async def main():
    browser = await launch(headless=False, userDataDir=DATA_DIR, args=['--no-sandbox'])
    page = await browser.newPage()

    # Go to the report1 website and login
    await page.goto(URL, waitUntil='networkidle0')
    if page.url != URL:
        await page.waitForSelector('.btnSendContainer')
        await page.type('input[type=tel]', USERNAME)
        await page.type('input[type=password]', PASSWORD)
        await page.click('.btnSendContainer')

    await page.waitForSelector('.commander__reports-row')
    await page.focus('nav a:nth-child(2)')
    await page.click('nav a:nth-child(2)')
    await page.waitForSelector('.commander__reports-row')

    # Create a new session and import the cookies
    cookies = await page.cookies()
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    # Get the statuses
    statuses_response = session.get("https://one.prat.idf.il/api/Attendance/getAllGroupsStatistics",
                                    headers=HEADERS_GET_STATUS)
    if statuses_response.status_code == HTTPStatus.OK:
        all_statuses = statuses_response.json()
        people_without_status = all_statuses['sectionsStatistics'][2]['membersStatistics']
        people_out_of_base = all_statuses['sectionsStatistics'][1]['membersStatistics']
        people_in_base = all_statuses['sectionsStatistics'][0]['membersStatistics']

        # Send report1 for Itai
        cookies = await page.cookies()
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        response = session.post("https://one.prat.idf.il/api/Attendance/updateAndSendPrat", headers=HEADERS_SEND_REPORT,
                                data=json.dumps({'mi': '',
                                                 'mainStatusCode': '01',
                                                 'secondaryStatusCode': '01',
                                                 'groupCode': '',
                                                 'note': ''}))

    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
