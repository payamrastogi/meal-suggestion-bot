import yaml

with open('config.yaml') as f:
    config_yaml = yaml.load(f, Loader=yaml.FullLoader)


def read_telegram_bot_token():
    return config_yaml['bot_token']
