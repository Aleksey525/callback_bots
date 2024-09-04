import argparse
import json
import os

import google.api_core.exceptions
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


def download_file(file_link, file_name):
    response = requests.get(file_link)
    response.raise_for_status()
    with open(file_name, 'wb') as file:
        file.write(response.content)


def main():
    env = Env()
    env.read_env()
    project_id = env.str('PROJECT_ID')
    json_file_url = env.str('JSON_FILE_URL')
    parser = argparse.ArgumentParser(
        description='Скрипт для обучения Dialogflow'
    )
    parser.add_argument('--file_url', default=json_file_url, type=str, help='learning_topic')
    args = parser.parse_args()
    url = args.file_url
    file_name = get_file_name(url)
    download_file(url, file_name)
    with open(file_name, 'r') as file:
        phrases_json = file.read()
    learning_topics = json.loads(phrases_json)
    for topic, phrases in learning_topics.items():
        try:
            display_name = topic
            training_phrases_parts = phrases['questions']
            message_texts = [phrases['answer'], ]
            create_intent(project_id, display_name, training_phrases_parts, message_texts)
        except google.api_core.exceptions.InvalidArgument:
            continue


if __name__ == '__main__':
    main()