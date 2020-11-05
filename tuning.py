import json
import requests


def tuning_reply(text):
    url = "http://www.tuling123.com/openapi/api"
    api_key = "49954564352843ad85afc997fb0acbe3"
    payload = {
        "key": api_key,
        "info": text,
        "userid": "666"
    }
    r = requests.post(url, data=json.dumps(payload))
    result = json.loads(r.content)
    if 'url' in result.keys():
        return result["text"] + result["url"]
    else:
        return result["text"]


if __name__ == '__main__':
    print(tuning_reply("你好"))
