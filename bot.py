import slack
from slack.errors import SlackApiError
import os


def post_msg(channel, msg):
    # todo: may configure token as env variable and use os.environ['SLACK_TOKEN']
    token = os.environ['SLACK_TOKEN']
    client = slack.WebClient(token)
    try:
      response = client.chat_postMessage(
        channel=channel,
        text=msg
      )
      print(response)
    except slack.errors.SlackApiError as e:
      print(e)


def main():
    post_msg("#my-bot", ":joy: \n :ox:")

    '''
    # token = os.environ['SLACK_TOKEN']
    try:
      client = slack.WebClient('your_token')
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
    client = slack.WebClient('your_token')
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


if __name__ == "__main__":
    main()
