import json
import os
import shutil
from typing import Any, Dict, List

from ..logging import log
from .coprocessor import Coprocessor
from .decorators import context
from .executor import SchemaExecutor
from .smartpipe import SmartPipe


def persist_schema(schema: Dict[str, Any]) -> None:
    if not os.path.exists("build"):
        os.makedirs("build")

    file_path = os.path.join("build", "workload.json")

    with open(file_path, "w") as file:
        json.dump(schema, file, indent=2)


def build() -> Dict[str, Any]:
    schema: Dict[str, Any] = {"smartpipes": {}}

    context.set_executor(SchemaExecutor())
    for sm in context.smart_pipes:
        sm.func("entry_point")

    for sm in context.smart_pipes:
        smartpipe: Dict[str, Any] = {
            "id": sm.id,
            "entry_point": {"type": "API", "path": sm.path, "method": sm.method},
            "coprocessors": [],
            "io": {},
        }

        for c in sm.coprocessors:
            coprocessor = {"id": c.id, "name": c.name, "type": c.type, "model": c.model}

            for source in c.sources:
                if not smartpipe["io"].get(source, None):
                    smartpipe["io"][source] = [c.id]
                else:
                    smartpipe["io"][source].append(c.id)

            smartpipe["coprocessors"].append(coprocessor)

        schema["smartpipes"][sm.id] = smartpipe

    persist_schema(schema)
    log.debug("Created Smart Pipes configuration")

    return schema
