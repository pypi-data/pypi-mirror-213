"""Module for ECS task definition rendering"""
import argparse
from json import dumps as json_dumps
import logging
from sys import exit as sys_exit
import botocore.exceptions
from boto3 import session as boto3_session
from profile_checker import ProfileChecker


item_to_be_remove_from_task_definition = ['taskDefinitionArn', 'revision', 'status', 'requiresAttributes', 'compatibilities', 'registeredAt', 'registeredBy']
image_list = []
logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.WARN)
parser = argparse.ArgumentParser(description='Render ECS task definition for update it')
parser.add_argument('-p', metavar='profile', help='Profile to use for task definition retrieve', default=None)
parser.add_argument('-f', metavar='family-name', help='Task definition family name')
parser.add_argument('-il', metavar='images-list', nargs='*', help='List of key=value that define images to be updated')


def clean_task_definition(task_definition: dict):
    for item in item_to_be_remove_from_task_definition:
        try:
            task_definition.pop(item)
        except:
            logging.warning(f'Ops, seems there is not \"{item}\" in the task definition')

def convert_dict_to_json(task_definition: dict):
    try:
        json_task_definition = json_dumps(task_definition, indent=4)
        return json_task_definition
    except:
        logging.error('Ops, something goes wrong during dict conversion to json')

def generate_client_session(profile: str, service: str):
    """Function to create a client session"""
    try:
        if profile is None:
            session = boto3_session.Session()
        else:
            session = boto3_session.Session(profile_name=profile)
        client = session.client(service)
        return client
    except botocore.exceptions.ClientError as error:
        logging.error(f'Ops, you encounter an exception: \"{error.response["Error"]["Code"]}\"')
        sys_exit(1)

def get_task_definition(client, family_name: str):
    try:
        task_definition = client.describe_task_definition(
            taskDefinition=family_name,
            include=['TAGS']
        )
        return task_definition.get('taskDefinition')
    except botocore.exceptions.ClientError as error:
        logging.error(f'Ops, you encounter an exception: \"{error.response["Error"]["Code"]}\"')
        sys_exit(1)

def parse_args(images: list):
    for item in images:
        try:
            key, value = item.split('=')
            image_list.append({key : value})
        except Exception as error:
            logging.error(f'Ops, something goes wrong: \"{error}\"')

def update_image_uri(task_definition: dict, containers_info: list):
    for definition in task_definition.get('containerDefinitions') or []:
        for item in containers_info:
            for k,v in item.items():
                if k == definition.get('name'):
                    definition['image'] = v

def main():
    """Main function"""
    args = parser.parse_args()
    profile = ProfileChecker(args.p).profile_name
    family_name = args.f
    images = args.il
    parse_args(images)
    ecs_client = generate_client_session(profile, 'ecs')
    task_definition = get_task_definition(ecs_client, family_name)
    clean_task_definition(task_definition)
    update_image_uri(task_definition, image_list)
    json_task_definition = convert_dict_to_json(task_definition)
    print(json_task_definition)

if __name__ == ('__main__' or '__init__'):
    try:
        main()
    except KeyboardInterrupt:
        pass
