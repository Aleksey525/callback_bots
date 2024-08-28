import json
import os
import requests
from urllib.parse import urlsplit, unquote

from environs import Env
from google.cloud import dialogflow


def create_intent(project_id, display_name, training_phrases_parts, message_texts):

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )
    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def get_file_name(file_link):
    splited_link = urlsplit(file_link)
    file_path = unquote(splited_link.path)
    splited_file_path = os.path.split(file_path)
    file_name = splited_file_path[1]
    return file_name


def download_file(file_link):
    response = requests.get(file_link)
    response.raise_for_status()
    file_name = get_file_name(file_link)
    with open(file_name, 'wb') as file:
        file.write(response.content)


def main():
    env = Env()
    env.read_env()
    project_id = env.str('PROJECT_ID')
    url = 'https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json'
    download_file(url)
    file_name = get_file_name(url)
    with open(file_name, 'r') as file:
        phrases_json = file.read()
    phrases = json.loads(phrases_json)
    display_name = 'Как устроиться к вам на работу'
    training_phrases_parts = phrases['Устройство на работу']['questions']
    message_texts = [phrases['Устройство на работу']['answer'], ]
    create_intent(project_id, display_name, training_phrases_parts, message_texts)


if __name__ == '__main__':
    main()