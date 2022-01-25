import slack
from slack.errors import SlackApiError
import os


def post_msg(channel, msg):
  # todo: may configure token as env variable and use os.environ['SLACK_TOKEN']
  token = 'replace_with_your_token'
  client = slack.WebClient(token)
  try:
    response = client.chat_postMessage(
      channel=channel,
      text=msg
    )
    print(response)
  except slack.errors.SlackApiError as e:
    print(e)

post_msg("#my-bot", ":joy: :ox:")

'''
# token = os.environ['SLACK_TOKEN']
try:
  client = slack.WebClient('xoxb-4916860785-2689773129490-BTv9P4somjNe7bALbUKzMVSv')
  response = client.chat_postMessage(channel="#my-bot", text=":joy: hello world from slackbot!")
except SlackApiError as e:
  print(e)
'''

block_contents = []
block_content = {}
block_content["type"] = "section"
block_text = {}
block_text["type"] = "mrkdwn"
block_text["text"] = ":ox: Danny Torrence left the following review for *your* property:"
block_content["text"] = block_text
block_contents.append(block_content)
client = slack.WebClient('xoxb-4916860785-2689773129490-BTv9P4somjNe7bALbUKzMVSv')
client.chat_postMessage(channel="#my-bot", blocks=block_contents)

'''
client.chat_postMessage(
  channel="#my-bot",
  blocks=[
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": ":ox: Danny Torrence left the following review for *your* property:"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "<https://example.com|Overlook Hotel> \n :star: \n Doors had too many axe holes, guest in room " +
          "237 was far too rowdy, whole place felt stuck in the 1920s."
      },
      "accessory": {
        "type": "image",
        "image_url": "https://images.pexels.com/photos/750319/pexels-photo-750319.jpeg",
        "alt_text": "Haunted hotel image"
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Average Rating*\n1.0"
        }
      ]
    }
  ]
)
'''
