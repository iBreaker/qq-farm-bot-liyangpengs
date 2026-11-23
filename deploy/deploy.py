#!/usr/bin/env python3
"""Activate an image already loaded and configured through ops on Linux02."""
import argparse
import json
import re
import shlex
import subprocess
import time


def remote(command):
    return subprocess.check_output(["ssh", "hub", "linux02", command], text=True)


def inspect():
    return json.loads(remote("sudo docker inspect --format " + shlex.quote(
        '{"image":{{json .Config.Image}},"id":{{json .Image}},'
        '"state":{{json .State.Status}},"health":{{json .State.Health.Status}}}'
    ) + " qq-farm-bot"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("check", "apply"))
    parser.add_argument("--image", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"qq-farm-bot:[a-zA-Z0-9_.-]+", args.image):
        parser.error("expected a local qq-farm-bot image tag")
    image = shlex.quote(args.image)
    expected_id = remote("sudo docker image inspect --format '{{.Id}}' " + image).strip()
    if args.action == "apply":
        # Configuration is exclusively published by ops-config-cli. Never edit it here.
        project = "/home/breaker/docker/linux02-qq-farm-bot"
        configured = remote("cd " + project + " && sudo docker compose config --format json")
        if json.loads(configured)["services"]["qq-farm-bot"]["image"] != args.image:
            raise SystemExit("publish the committed Compose through ops before activation")
        remote("cd " + project + " && sudo docker compose up -d --pull never "
               "--no-build --no-deps --force-recreate qq-farm-bot")
    deadline = time.monotonic() + (120 if args.action == "apply" else 0)
    while True:
        state = inspect()
        good = (state["image"] == args.image and state["id"] == expected_id
                and state["state"] == "running" and state["health"] == "healthy")
        if good or time.monotonic() >= deadline:
            print(json.dumps(state))
            return 0 if good else 1
        time.sleep(5)


if __name__ == "__main__":
    raise SystemExit(main())
