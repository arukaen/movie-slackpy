<img align="right" src="http://i.imgur.com/Xk1qB3A.png" height="389" width="176">

# movie-slackpy : Custom slash command for Slack

## What is it?
A script in Python that lets you easily share/lookup a movie in Slack.

## Setting up Slack
1. Create a Slack [Incoming Webhook](https://my.slack.com/services/new/incoming-webhook/). Take note of the Webhook URL as that is important. The rest of the settings are not.
2. Deploy your copy of `movie-slackpy` and make sure it is accessible via an endpoint.
3. Create a Slack [Slash Command](https://my.slack.com/services/new/slash-commands). Be sure to set your method to POST and set your URL endpoint from Step #2. All the other options are optional.

## Environment
The following environment variables need to be set!

- `BOT_NAME` - The username in which the webhook should respond with. Defaults to whatever it set on the webhook configuration.
- `EMOJI` - The emoji to use with the webhook response. Defaults to whatever it set on the webhook configuration.
- `SLACK_WEBHOOK_URL` - Slack [Incoming Webhook](https://my.slack.com/services/new/incoming-webhook/) URL.
- `TMDB_API_KEY` - Your [API Key](https://developers.themoviedb.org/3/getting-started) for The Movie Database

## Deploy with Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/arukaen/movie-slackpy)

Click the button above to launch the app via Heroku.

## How to contribute !
I am open to all feedback, bug reports, and pull requests!

## To-do
- [ ] Add `tv` show support. 