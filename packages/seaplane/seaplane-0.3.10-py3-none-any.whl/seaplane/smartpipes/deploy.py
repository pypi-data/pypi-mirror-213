import json
import os
import shutil

from typing import Any, Dict, List

from .decorators import context
from .coprocessor import Coprocessor
from ..logging import log
from .build import build
from ..configuration import config

import requests

from ..api.api_http import headers
from ..api.api_request import provision_req
from ..util import unwrap


def create_coprocessor_docker_file(coprocessor: Coprocessor) -> None:
    docker_file = f"""FROM python:3.10

ENV SMARTPIPES_PRODUCTION True
ENV COPROCESSOR_ID {coprocessor.id}
WORKDIR /app
COPY . . 

RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python", "demo.py"]
    """

    if not os.path.exists(f"build/{coprocessor.id}"):
        os.makedirs(f"build/{coprocessor.id}")

    with open(f"build/{coprocessor.id}/Dockerfile", "w") as file:
        file.write(docker_file)


def create_http_api_entry_point() -> None:
    docker_file = """FROM python:3.10

ENV SMARTPIPES_PRODUCTION True
ENV PORT 5000

WORKDIR /app
COPY . . 

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn


EXPOSE 5000

CMD gunicorn --bind 0.0.0.0:${PORT} --workers 5 --timeout 300 demo:sea
    """

    if not os.path.exists(f"build/http"):
        os.makedirs(f"build/http")

    with open("build/http/Dockerfile", "w") as file:
        file.write(docker_file)


def create_carrier_workload_file(
    smart_pipe_id: str, coprocessor: Coprocessor, next_coprocessors: List[str]
) -> None:
    output = None

    if len(next_coprocessors) > 1:
        output = {
            "broker": {
                "outputs": map(
                    lambda c_id: {"carrier": {"subject": f"{smart_pipe_id}.{c_id}"}},
                    next_coprocessors,
                )
            }
        }
    elif len(next_coprocessors) == 1:
        output = {
            "label": "carrier_out",
            "carrier": {"subject": f"{smart_pipe_id}.{next_coprocessors[0]}"},
        }

    workload = {
        "tenant": "tnt-0oqdcinn0pubb000tq8ng6qoos",
        "id": coprocessor.id,
        "input": {
            "label": "carrier_in",
            "carrier": {
                "subject": f"{smart_pipe_id}.{coprocessor.id}",
                "deliver": "all",
                "queue": coprocessor.id,
            },
        },
        "processor": {
            "docker": {
                "image": f"us-central1-docker.pkg.dev/artifacts-356722/demo/coprocessors/{coprocessor.id}:latest",
                "args": [],
            }
        },
        "output": output,
    }

    if not os.path.exists(f"build/{coprocessor.id}"):
        os.makedirs(f"build/{coprocessor.id}")

    with open(f"build/{coprocessor.id}/workload.json", "w") as file:
        json.dump(workload, file, indent=2)
        log.debug(f"Created {coprocessor.id} workload")

    return workload


def copy_project_into_coprocessors(coprocessor: Coprocessor) -> None:
    source_folder = "."
    destination_folder = f"build/{coprocessor.id}"

    for item in os.listdir(source_folder):        
        if os.path.isdir(item) and item == "build":
            continue  # Skip the "build" folder

        destination_path = os.path.join(destination_folder, item)
        shutil.copy2(item, destination_path)


def create_stream(name: str) -> Any:
    log.debug(f"Creating stream: {name}")
    url = f"{config.carrier_endpoint}/stream/{name}"
    req = provision_req(config._token_api)

    payload = {
        "message_ttl": 3600,
        "max_messages": 1000000,
        "max_size": 100000000,
        "replicas": 3,
        "allow_locations": ["region/xn"],
        "deny_locations": ["country/nl"],
        "wait_for_ack": True,
        "ack_timeout": 5,
        "max_delivery_attempts": 5,
        "max_delivery_time": 60,
        "dead_letter_sink": "dead-letter-sink"
    }

    return unwrap(
        req(
            lambda access_token: requests.put(
                url,
                json=payload,
                headers=headers(access_token),
            )
        )
    )


def delete_stream(name: str) -> Any:
    log.debug(f"Deleting stream: {name}")
    url = f"{config.carrier_endpoint}/stream/{name}"
    req = provision_req(config._token_api)

    return unwrap(
        req(
            lambda access_token: requests.delete(
                url,
                headers=headers(access_token),
            )
        )
    )


def create_flow(name: str, workload: Dict[str, Any]) -> Any:
    log.debug(f"Creating flow: {name}")
    url = f"{config.carrier_endpoint}/flow/{name}"
    req = provision_req(config._token_api)

    return unwrap(
        req(
            lambda access_token: requests.put(
                url,
                json=workload,
                headers=headers(access_token),
            )
        )
    )


def delete_flow(name: str) -> Any:
    log.debug(f"Deleting flow: {name}")

    url = f"{config.carrier_endpoint}/flow/{name}"
    req = provision_req(config._token_api)

    return unwrap(
        req(
            lambda access_token: requests.delete(
                url,                
                headers=headers(access_token),
            )
        )
    )


def deploy() -> None:
    schema = build()

    for sm in context.smart_pipes:
        delete_stream(sm.id)
        create_stream(sm.id)

        for c in sm.coprocessors:
            delete_flow(c.id)

            create_coprocessor_docker_file(c)
            next_coprocessors = schema["smartpipes"][sm.id]["io"].get(c.id, None)

            if next_coprocessors is None:
                next_coprocessors = []

            workload = create_carrier_workload_file(sm.id, c, next_coprocessors)
            copy_project_into_coprocessors(c)

            create_flow(c.id, workload)

            log.info(f"Deploy for coprocessor {c.id} done")

    create_http_api_entry_point()
    log.info(f"Build for coprocessor {c.id} done")
