from __future__ import print_function

import base64
import json
import urllib2

TIMEOUT = 1


def validate_url(url):
    request = urllib2.urlopen(url, timeout=TIMEOUT)
    json_body = json.load(request)
    last_datapoint = json_body['bgs'][0]['sgv']
    return last_datapoint


def canonicalize_url(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    if not url.endswith('/'):
        url = url + '/'
    url = url + 'pebble'
    return url


def lambda_handler(event, context):
    query = event['queryStringParameters']
    url = query['url']
    canonical_url = canonicalize_url(url)
    last_datapoint = validate_url(canonical_url)
    token = base64.urlsafe_b64encode(canonical_url)
    return {
        'statusCode': '200',
        'body': json.dumps({
            'canonical_url': canonical_url,
            'last_datapoint': last_datapoint,
            'token': token
        }),
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json',
        },
    }
