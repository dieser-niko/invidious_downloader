import requests
import json
import os
import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("videoId", help="Video ID")
    parser.add_argument("-t", "--timeout", help="Timeout before switching to next instance.", default=3)
    parser.add_argument("-s", "--successFile", help="Path to success rate file. Saves preferred instances.", default="successrate.json")
    return parser.parse_args()


session = requests.Session()
all_instances = session.get("https://api.invidious.io/instances.json").json()


def change_rate(rates, uri, success: bool):
    print("+" if success else "-", uri)
    rate = rates.get(uri, (0,0))
    rates[uri] = (rate[0] + success, rate[1] + 1)

def get_rate(inp):
    return inp[0] / inp[1]

def download(video_id, timeout=3, success_file="successrate.json"):
    try:
        with open(success_file, "r") as fobj:
            success_rates = json.load(fobj)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        success_rates = dict()

    instances = sorted(all_instances, key=lambda a: get_rate(success_rates.get(a[1]["uri"], (1,1))))

    for name, instance in instances[::-1]:
        if instance["type"] != "https":
            continue
        print("~", instance["uri"], end="\r")
        try:
            vid_info = session.get(f"{instance['uri']}/api/v1/videos/{video_id}", timeout=timeout).json()
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError, requests.exceptions.JSONDecodeError):
            change_rate(success_rates, instance["uri"], False)
            continue
        success = False
        for _format in sorted(vid_info["adaptiveFormats"], key=lambda a: a.get("bitrate", 0)):
            if "container" not in _format:
                continue
            response = session.get(_format["url"])
            if response.status_code != 200:
                continue
            top_format = response.content
            file_name = f"output.{_format['container']}"
            with open(file_name, "wb") as fobj:
                fobj.write(response.content)
            success = True
            break
        change_rate(success_rates, instance["uri"], success)
        if success:
            break
    with open(success_file, "w") as fobj:
        json.dump(success_rates, fobj)
    return file_name if success else None


if __name__ == "__main__":
    args = parse_args()
    print(download(args.videoId))
    