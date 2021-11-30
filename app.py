import os
import requests
import sys
import tmdbsimple as tmdb
from flask import Flask, abort, json, request
from datetime import timedelta

botName = os.getenv('BOT_NAME')
emoji = os.getenv('EMOJI')
token = os.getenv('SLACK_TOKEN')
hookURL = os.getenv('SLACK_WEBHOOK_URL')
tmdbKey = os.getenv('TMDB_API_KEY')

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
	movieQuery = request.form.get('text', None)
	channel_id = request.form.get('channel_id', None)
	tmdb.API_KEY = tmdbKey
	search = tmdb.Search()
	search.movie(query=movieQuery)
	details = tmdb.Movies(int(search.results[0]['id'])).info()

	slack_data = {
		"username": botName,
		"icon_emoji": emoji,
		"channel": channel_id,
		"attachments": [{
		"title": search.results[0]['title'],
		"title_link": 'https://www.themoviedb.org/movie/' + str(search.results[0]['id']) + '-' + search.results[0]['title'].lower(),
		"color": '#FFB10A',
		"image_url": 'https://image.tmdb.org/t/p/w640' + search.results[0]['poster_path'],
		"fields": [{
		  "title": 'Rating',
		  "value": str(search.results[0]['vote_average']) + ' (' + str(search.results[0]['vote_count']) + ' votes)',
		  "short": True
		}, {
		  "title": 'Year',
		  "value": search.results[0]['release_date'],
		  "short": True
		}, {
		  "title": 'Runtime',
		  "value": str(timedelta(minutes=details['runtime']))[:-3],
		  "short": True
		}, {
		  "title": 'Revenue',
		  "value": '$' + format(details['revenue'], ',.2f'),
		  "short": True
		}, {
		  "title": 'Overview',
		  "value": search.results[0]['overview'],
		  "short": False
		}]
		}]
	}

	slack_post = requests.post(hookURL, json=slack_data, headers={'Content-Type': 'application/json'})
	print(slack_data)

	if slack_post.status_code != 200:
		raise ValueError(
			'Request to slack returned an error %s, the response is:\n%s'
			% (slack_post.status_code, slack_post.text)
		)
	elif slack_post.status_code == 200:
		return ('', 200)


if __name__ == "__main__":
        app.run()
