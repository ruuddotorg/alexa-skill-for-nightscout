from __future__ import print_function

import base64
import urllib2
import json


def get_bg_sentence(nightscout_url):
    data = json.load(urllib2.urlopen(nightscout_url, timeout=1))

    now = data['status'][0]['now']
    bg = data['bgs'][0]
    time_ago = int((float(now) - float(bg['datetime'])) / 60000.0)
    bg_value = bg['sgv']

    if time_ago < 0:
        time_period = 'in the future'
    elif time_ago <= 1:
        time_period = 'a minute ago'
    else:
        time_period = '{} minutes ago'.format(time_ago)

    trend_map = {
        1: 'rapidly rising',
        2: 'rising',
        3: 'slowly rising',
        4: 'flat',
        5: 'slowly falling',
        6: 'falling',
        7: 'rapidly falling'
    }
    trend_string = trend_map.get(bg['trend'])

    sentence = '{} the value was {}'.format(time_period, bg_value)
    if trend_string is not None:
        sentence += ' and {}'.format(trend_string)

    return sentence


def link_account():
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': 'Please use the Alexa app to link your Nightscout server.',
        },
        'card': {
            'type': 'LinkAccount',
        },
        'reprompt': {},
        'shouldEndSession': True
    }


def nightscout_value(nightscout_url):
    sentence = get_bg_sentence(nightscout_url)
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': sentence,
        },
        # No card, it is confusing to see past BG values in the Alexa app.
        'reprompt': {},
        'shouldEndSession': True
    }


def lambda_handler(event, context):
    access_token = event['session']['user'].get('accessToken')
    if access_token is not None:
        nightscout_url = base64.urlsafe_b64decode(access_token.encode('utf-8'))
        response = nightscout_value(nightscout_url)
    else:
        response = link_account()
    return {
        'version': '1.0',
        'sessionAttributes': {},
        'response': response
    }
