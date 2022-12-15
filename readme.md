<h1 align="center">
  <br>
  <img src="https://i.imgur.com/Zx3BTJG.png" alt="Logo" height="312" width="312"/>
  <br>
  <span style="color:#0a4359;">Movie Bot</span>
  <br>
</h1>

# movie-slackpy : Custom command for Slack

## What is it?
A script in Python that lets you easily share/lookup a movie in Slack.

## Setting up Slack
1. Create a Slack [Incoming Webhook](https://my.slack.com/services/new/incoming-webhook/). Take note of the Webhook URL as that is important. The rest of the settings are not.
2. Deploy your copy of `movie-slackpy` and make sure it is accessible via an endpoint.
3. Create a Slack [Slash Command](https://my.slack.com/services/new/slash-commands). Be sure to set your method to POST and set your URL endpoint from Step #2. All the other options are optional.

## Environment
The following environment variables need to be set!

- `BOT_NAME` - The username in which the webhook should respond with. Defaults to whatever it set on the webhook configuration. (Default: Meseeks)
- `EMOJI` - The emoji to use with the webhook response. Defaults to whatever it set on the webhook configuration. (Deafault: :movie_camera:)
- `SLACK_WEBHOOK_URL` - Slack [Incoming Webhook](https://my.slack.com/services/new/incoming-webhook/) URL. (REQUIRED)
- `OMDB_API_KEY` - Your [API Key](https://www.omdbapi.com/apikey.aspx) for OMDB API.

## Deploy with Serverless + AWS
[![Deploy](https://assets-global.website-files.com/60acbb950c4d6606963e1fed/611631cd314b2abec6c29ec0_bolt.svg)](https://www.serverless.com/framework/docs/getting-started)
[![Deploy](


## How to contribute !
I am open to all feedback, bug reports, and pull requests!

## To-do
- [ ] Add `imdbID` support.
- [ ] Add searching by year.
- [ ] Add tests.
