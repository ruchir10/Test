import os
import boto3
import json

def get_aws_secrets(secret_name):

    session = boto3.session.Session()
    client = session.client('secretsmanager')


    response = client.get_secret_value(SecretId=secret_name)

    if 'SecretString' in response:
        secret = json.loads(response['SecretString'])
        return secret
    else:
        raise ValueError('Failed to retrieve secret.')

def create_config_file(secret, directory):
    config = {}

    if 'AWS_ACCESS_KEY_ID' in secret:
        config['AWS_ACCESS_KEY'] = secret['AWS_ACCESS_KEY_ID']
    else:
        raise ValueError('AWS_ACCESS_KEY_ID not found in secret.')

    if 'AWS_SECRET_ACCESS_KEY' in secret:
        config['AWS_SECRET_KEY'] = secret['AWS_SECERET_ACCESS_KEY']
    else:
        raise ValueError('AWS_SECERET_ACCESS_KEY not found in secret.')

    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, 'config.json')

    with open(file_path, 'w') as file:
        json.dump(config, file, indent=4)

if __name__ == '__main__':
    secret_name = 'awsDemo' 
    directory = 'temp' 

    try:
        secret = get_aws_secrets(secret_name)
        create_config_file(secret, directory)
        print(f'config.json file created successfully in {directory}.')
    except Exception as e:
        print(f'Error: {str(e)}')
