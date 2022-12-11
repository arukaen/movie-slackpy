from urllib.parse import parse_qsl
import requests
import json
import os

bot_name = os.environ.get('BOT_NAME', 'Meseeks')
emoji = os.environ.get('EMOJI', ":movie_camera:")
omdb_key = os.environ.get('OMDB_API_KEY')
omdb_url = 'https://www.omdbapi.com/'
slack_webhook_url = os.environ.get('SLACK_WEBHOOK_URL')

def omdb_query(movie):
    payload = {'apikey': omdb_key, 't': movie}
    response = requests.get(omdb_url, params=payload)
    result = json.loads(response.txt)
    return result

def handler(event, context):
  # Ensure the request method is POST
  if event['httpMethod'] != 'POST':
    return {
      'statusCode': 405,
      'body': 'Method Not Allowed',
    }

  # Ensure the request content-type is "application/x-www-form-urlencoded"
  if event['headers']['content-type'] != 'application/x-www-form-urlencoded':
    return {
      'statusCode': 400,
      'body': 'Bad Request',
    }

  # Parse the form data
  body = event['body']
  parsed = dict(parse_qsl(body))

  search_term = parsed["text"]
  channel_id = parsed["channel_id"]

  results = omdb_query(search_term)

  response_data = {
        "username": bot_name,
        "icon_emoji": emoji,
        "channel": channel_id,
        "attachments": [{
            "title": results["Title"],
            "title_link": "https://www.imdb.com/title/" + results["imdbID"],
            "color": "#7B00FF",
            "image_url": results["Poster"],
            "fields": [{
                "title": "Rating",
                "value": rating,
                "short": True,
            },
            {
                "title": "Year",
                "value": results["Year"],
                "short": True,
            },
            {
                "title": "Runtime",
                "value": results["Runtime"],
                "short": True,
            },
            {
                "title": "Director",
                "value": results["Director"],
                "short": True,
            },
            {
                "title": "Actors",
                "value": results["Actors"],
            }]
        }]
    }

  return_content = requests.post(slack_webhook_url, json=response_data, headers={'Content-Type': 'application/json'})


  # Return a success response
  return {
    'statusCode': 200,
    'body': '',
  }
