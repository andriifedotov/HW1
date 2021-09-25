import requests
import json
import os

from requests.exceptions import HTTPError

from config import Config

def app(config):

    os.makedirs(os.path.join(config['API']['directory'], config['API']['payload']['date']), exist_ok=True)

    try:
        url = config['API']['url']
        headers = {"content-type": config['AUTH']['content-type']}
        data = config['AUTH']['payload']
        r = requests.post(url+config['AUTH']['endpoint'], headers=headers, data=json.dumps(data))
        token = r.json()['access_token']

        headers = {"content-type": config['API']['content-type'], "Authorization": config['AUTH']['Authorization'] + token}
        data = {"date": config['API']['payload']['date']}
        r = requests.get(url+config['API']['endpoint'], headers=headers, data=json.dumps(data))

        r.raise_for_status()

        with open(os.path.join(config['API']['directory'], config['API']['payload']['date'],
                               config['API']['payload']['date'] + '.json'), 'w') as json_file:
            data = r.json()
            json.dump(data, json_file)
    except HTTPError:
        print('Error!')


if __name__ == '__main__':
    config = Config(os.path.join('.', 'config.yaml'))

    app(
            config=config.get_config('app')
        )