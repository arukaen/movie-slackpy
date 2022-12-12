from urllib.parse import parse_qsl
import requests
import json
import os

bot_name = os.environ.get('BOT_NAME', 'Meseeks')
emoji = os.environ.get('EMOJI', ":movie_camera:")
omdb_key = os.environ.get('OMDB_API_KEY')
omdb_url = 'https://www.omdbapi.com/'
slack_webhook_url = os.environ.get('SLACK_WEBHOOK_URL')

# Check if the required environment variables are set
if omdb_key is None:
    raise ValueError('Missing required environment variable: OMDB_API_KEY')
if slack_webhook_url is None:
    raise ValueError('Missing required environment variable: SLACK_WEBHOOK_URL')

def omdb_query(movie):
    """Queries the Open Movie Database (OMDB) API for information about the given movie.

    Args:
        movie (str): The title of the movie to search for.

    Returns:
        dict: A dictionary containing the specified fields from the OMDB API response.

    Raises:
        requests.exceptions.RequestException: If an error occurs while making the request to the OMDB API.
    """

    payload = {'apikey': omdb_key, 't': movie}

    try:
        response = requests.get(omdb_url, params=payload)
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.RequestException as error:
        print('An error occurred while making the request: {}'.format(error))
        return None

    fields = [
        'Title',
        'imdbID',
        'Poster',
        'imdbRating',
        'imdbVotes',
        'Year',
        'Runtime',
        'Director',
        'Actors',
        'Plot',
    ]
    data = {field: result[field] for field in fields}

    print('OMDB query successful for movie: {}'.format(movie))
    return data


def handler(event, context):
    # Ensure the request method is POST
    if event['httpMethod'] != 'POST':
        return {
            'statusCode': 405,
            'body': 'Method Not Allowed',
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
                "value": results["imdbRating"] + ' (' + results["imdbVotes"] + ' votes)',
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
            },
            {
                "title": "Overview",
                "value": results["Plot"],
                "short": False,
            }]
        }]
    }

    try:
        requests.post(slack_webhook_url, json=response_data, headers={'Content-Type': 'application/json'})
    except requests.exceptions.RequestException as e:
        # Handle exceptions here
        print("Error occurred while sending data to Slack: {}".format(e))

    # Return a success response
    return {
        'statusCode': 200,
        'body': '',
    }
