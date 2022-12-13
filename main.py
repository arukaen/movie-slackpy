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

def send_slack_message(movie_data, slack_channel):
    """
    Sends the given data to Slack using a webhook.

    Args:
        movie_data: The data to be sent to Slack.
        slack_channel: The Slack channel to send the data to.

    Returns:
        The response from the POST request, or None if an error occurred.
    """    
    # Send a message to Slack with the requested movie
    
    response_data = {
        "username": bot_name,
        "icon_emoji": emoji,
        "channel": slack_channel,
        "attachments": [{
            "title": movie_data["Title"],
            "title_link": "https://www.imdb.com/title/" + movie_data["imdbID"],
            "color": "#7B00FF",
            "image_url": movie_data["Poster"],
            "fields": [{
                "title": "Rating",
                "value": movie_data["imdbRating"] + ' (' + movie_data["imdbVotes"] + ' votes)',
                "short": True,
            },
            {
                "title": "Year",
                "value": movie_data["Year"],
                "short": True,
            },
            {
                "title": "Runtime",
                "value": movie_data["Runtime"],
                "short": True,
            },
            {
                "title": "Director",
                "value": movie_data["Director"],
                "short": True,
            },
            {
                "title": "Actors",
                "value": movie_data["Actors"],
            },
            {
                "title": "Overview",
                "value": movie_data["Plot"],
                "short": False,
            }]
        }]
    }

    try:
        response = requests.post(
            slack_webhook_url,
            json=response_data,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while sending data to Slack: {e}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"An HTTP error occurred while sending data to Slack: {e}")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"A connection error occurred while sending data to Slack: {e}")
        return None
    except requests.exceptions.Timeout as e:
        print(f"The request timed out while sending data to Slack: {e}")
        return None

    print("Data successfully sent to Slack")
    return response



def handler(event, context):
    """
    Request handler for an AWS Lambda function.
    
    Args:
        event: A dictionary containing data about the HTTP request.
        context: A dictionary containing runtime information for the Lambda function.
        
    Returns:
        A dictionary containing the response data.
        
    Raises:
        requests.exceptions.RequestException: If there is an error while sending the data to Slack.
    """
        
    # Ensure the request method is POST
    if event['httpMethod'] != 'POST':
        return {
            'statusCode': 405,
            'body': 'Method Not Allowed',
        }

    # Parse the form data
    body = event['body']
    parsed = dict(parse_qsl(body))

    # Ensure the required fields are present
    required_fields = ["text", "channel_id"]
    for field in required_fields:
        if field not in parsed:
            return {
                'statusCode': 400,
                'body': f"Missing required field: {field}"
            }

    search_term = parsed["text"]
    channel_id = parsed["channel_id"]

    try:
        results = omdb_query(search_term)
        send_slack_message(results, channel_id)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

    # Return a success response
    return {
        'statusCode': 200,
        'body': '',
    }