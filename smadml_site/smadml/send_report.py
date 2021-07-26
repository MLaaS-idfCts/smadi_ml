import asyncio
import json
import os

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


async def __main(mi: int) -> None:
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
    [session.cookies.set(cookie['name'], cookie['value']) for cookie in cookies]

    group_code = await page.evaluate("() => document.querySelector('nav > a').text")
    group_code = group_code.split(' ')[1]

    session.post("https://one.prat.idf.il/api/Attendance/updateAndSendPrat", headers=HEADERS_SEND_REPORT,
                 data=json.dumps({'mi': mi,
                                  'mainStatusCode': '01',
                                  'secondaryStatusCode': '01',
                                  'groupCode': group_code,
                                  'note': ''}))

    await browser.close()


def send_report(mi: str) -> None:
    """
    Send report
    :param mi: ID num
    :type mi:str
    :return: None
    :rtype: None
    """
    asyncio.get_event_loop().run_until_complete(__main(int(mi)))
