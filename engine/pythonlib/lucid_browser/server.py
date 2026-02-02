import subprocess
from pathlib import Path
from typing import Any, Dict, NoReturn, Tuple, Union
import json
import os

import base64
import orjson
from playwright._impl._driver import compute_driver_executable

from lucid_browser.pkgman import LOCAL_DATA
from lucid_browser.utils import launch_options

LAUNCH_SCRIPT: Path = LOCAL_DATA / "launchServer.js"


def camel_case(snake_str: str) -> str:
    """
    Convert a string to camelCase
    """
    if len(snake_str) < 2:
        return snake_str
    camel_case_str = ''.join(x.capitalize() for x in snake_str.lower().split('_'))
    return camel_case_str[0].lower() + camel_case_str[1:]


def to_camel_case_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert a dictionary to camelCase
    """
    return {camel_case(key): value for key, value in data.items()}


def get_nodejs() -> str:
    """
    Get the bundled Node.js executable
    """
    # Note: Older versions of Playwright return a string rather than a tuple.
    _nodejs: Union[str, Tuple[str, ...]] = compute_driver_executable()[0]
    if isinstance(_nodejs, tuple):
        return _nodejs[0]
    return _nodejs


def launch_server(fingerprint=None, **kwargs) -> NoReturn:
    """
    Launch a Playwright server. Takes the same arguments as `Lucid Empire()`.
    Prints the websocket endpoint to the console.
    
    Args:
        fingerprint (str): Path to the Golden Template JSON. MANDATORY.
    """
    # 1. Enforce Template Existence (Fail-Closed)
    if fingerprint is None:
        raise ValueError(
            "LUCID CORE PANIC: No Golden Template provided. "
            "Randomization Protocols Disabled. You must provide a "
            "path to a validated 'Golden Template' JSON."
        )

    # 2. JSON Template Ingestion
    config_data = {}
    if isinstance(fingerprint, str):
        if not os.path.exists(fingerprint):
            raise FileNotFoundError(
                f"LUCID PANIC: Template file not found at {fingerprint}"
            )
        
        try:
            with open(fingerprint, 'r') as f:
                config_data = json.load(f)
        except json.JSONDecodeError:
            raise ValueError("LUCID PANIC: Corrupted Golden Template JSON.")
    else:
        # Support direct dictionary injection
        config_data = fingerprint

    # 3. Schema Validation
    required_vectors = ['navigator', 'screen', 'webgl', 'fonts']
    for vector in required_vectors:
        if vector not in config_data:
            raise ValueError(
                f"LUCID PANIC: Invalid Template Structure. "
                f"Missing critical vector: {vector}"
            )

    # Inject config
    kwargs['config'] = config_data

    config = launch_options(**kwargs)
    nodejs = get_nodejs()

    data = orjson.dumps(to_camel_case_dict(config))

    process = subprocess.Popen(  # nosec
        [
            nodejs,
            str(LAUNCH_SCRIPT),
        ],
        cwd=Path(nodejs).parent / "package",
        stdin=subprocess.PIPE,
        text=True,
    )
    # Write data to stdin and close the stream
    if process.stdin:
        process.stdin.write(base64.b64encode(data).decode())
        process.stdin.close()

    # Wait forever
    process.wait()

    # Add an explicit return statement to satisfy the NoReturn type hint
    raise RuntimeError("Server process terminated unexpectedly")
