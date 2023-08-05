# Implement the lifecycle commands here
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
from tempfile import gettempdir
import requests
import boto3
from cement import minimal_logger

from hmd_cli_tools import cd
from hmd_cli_neuronsphere.hmd_cli_neuronsphere import (
    start_neuronsphere,
    stop_neuronsphere,
    run_local_service,
)
from hmd_cli_tools.prompt_tools import prompt_for_values
from typing import Dict

import yaml

logger = minimal_logger(__name__)


minio_script = """
curl https://dl.min.io/client/mc/release/linux-amd64/mc \
  --create-dirs \
  -o $HOME/minio-binaries/mc

chmod +x $HOME/minio-binaries/mc
export PATH=$PATH:$HOME/minio-binaries/

mc alias set localminio http://minio:9000 {access_key} {secret_key}
mc admin config set localminio/ notify_webhook:{repo_name} \
    endpoint="http://proxy/{instance_name}/apiop/handle_events"
mc admin service restart localminio
mc event add localminio/{bucket_name} arn:minio:sqs::{repo_name}:webhook \
  --event put,delete
"""


def _start_local_ns():
    config_overrides = {
        "trino": False,
        "jupyter": False,
        "apache_superset": False,
        "transform": False,
    }
    try:
        healthcheck = requests.get("http://localhost/health-check")

        if healthcheck.status_code != 200:
            start_neuronsphere(config_overrides=config_overrides)
    except Exception as e:
        start_neuronsphere(config_overrides=config_overrides)


def validate_config(config: Dict) -> bool:
    valid = True

    if "content_item_paths" not in config:
        logger.error("Invalid Config: missing 'content_item_paths' property")
        valid = False

    if "content_items_paths" in config and not isinstance(
        config["content_item_paths"], dict
    ):
        logger.error("Invalid Config: 'content_item_paths' must be a dictionary")
        valid = False

    return valid


def update_setup_py(setup_path: Path, repo_name: str):
    with open(setup_path, "r") as setup:
        setup_data = setup.read().splitlines()

    output = []
    found = False
    for line in setup_data:
        if line.strip().startswith('name="hmd-lang-local-librarian",'):
            found = True
            indent = line.index("name")
            output.append((" " * indent) + f'name="{repo_name}",')
        else:
            output.append(line)
    if not found:
        raise Exception("setup.py doesn't contain an empty 'name' line.")
    with open(setup_path, "w") as setup:
        setup.writelines(f"{line}\n" for line in output)


def build():
    pass


def publish():
    pass


def deploy():
    pass


def start(config_file: str = "./src/configs/default.librarian.json"):
    _start_local_ns()

    librarian_cfg_path = Path(config_file)

    if not os.path.exists(librarian_cfg_path):
        raise Exception(f"Cannot find Librarian configuration file at {config_file}")

    with open(librarian_cfg_path, "r") as cfg:
        librarian_cfg = json.load(cfg)

    if not validate_config(librarian_cfg):
        return

    root_path = Path("./").absolute()

    schemas_path = root_path / Path(librarian_cfg.get("schemas", "./src/schemas"))

    if not os.path.exists(schemas_path):
        raise Exception("Cannot find schemas.")

    cit_path = root_path / Path(
        librarian_cfg.get(
            "content_item_types", "./src/entities/hmd_lang_librarian.content_item_types"
        )
    )

    if not os.path.exists(cit_path):
        raise Exception("Cannot find ContentItemTypes")

    repo_name = os.path.basename(os.getcwd())
    _dirname = Path(os.path.dirname(__file__))
    _librarian_dir = _dirname / "local_librarian_prj"

    tmpdir = gettempdir()
    tmp_path = Path(tmpdir)

    shutil.copytree(_librarian_dir, tmp_path / repo_name, dirs_exist_ok=True)

    with open(tmp_path / repo_name / "meta-data" / "manifest.json", "r") as mf:
        manifest = json.load(mf)

    manifest["global_variables"] = {
        "base_package": repo_name.replace("-", "_"),
        "package_name": repo_name.replace("-", "_"),
    }

    with open(tmp_path / repo_name / "meta-data" / "manifest.json", "w") as mf:
        json.dump(manifest, mf)

    with open(tmp_path / repo_name / "meta-data" / "config_local.json", "r") as cfg:
        config_local = json.load(cfg)

    config_local["loader_config"] = {"local": ["hmd-lang-librarian", repo_name]}

    config_local["hmd_db_engines"]["dynamo"]["engine_config"][
        "dynamo_table"
    ] = f"{repo_name}-librarian"

    with open(tmp_path / repo_name / "meta-data" / "config_local.json", "w") as cfg:
        json.dump(config_local, cfg)

    with open(Path(os.getcwd()) / "meta-data" / "config_local.json", "w") as cfg:
        json.dump(config_local, cfg)

    update_setup_py(tmp_path / repo_name / "src" / "python" / "setup.py", repo_name)

    shutil.copytree(
        schemas_path, tmp_path / repo_name / "src" / "schemas", dirs_exist_ok=True
    )
    shutil.copytree(cit_path, tmp_path / repo_name / "src" / "cit", dirs_exist_ok=True)
    with cd(tmp_path / repo_name):
        session = boto3.Session()

        credentials = {
            "access_key": "dummykey",
            "secret_key": "dummykey",
            "token": None,
        }
        if "bucket_name" in librarian_cfg:
            creds = session.get_credentials()
            credentials = {
                "access_key": creds.access_key,
                "secret_key": creds.secret_key,
                "token": creds.token,
            }

        s3_endpoint = None
        bucket_name = f"{repo_name}-default-bucket"
        if "bucket_name" not in librarian_cfg:
            s3_endpoint = "http://minio:9000/"
            session = boto3.Session(
                aws_access_key_id="minioadmin", aws_secret_access_key="minioadmin"
            )

            credentials["access_key"] = "minioadmin"
            credentials["secret_key"] = "minioadmin"
            credentials["token"] = None

            s3_client = session.client("s3", endpoint_url="http://localhost:9000")
            try:
                s3_client.create_bucket(Bucket=bucket_name)
            except:
                pass

            with open("minio_config.sh", "w") as mc:
                mc.write(
                    minio_script.format(
                        bucket_name=bucket_name,
                        repo_name=repo_name,
                        instance_name=repo_name.replace("-", "_"),
                        access_key=credentials["access_key"],
                        secret_key=credentials["secret_key"],
                    )
                )

        default_docker_compose = {
            "services": {
                repo_name.replace("-", "_"): {
                    "image": f"{os.environ.get('HMD_CONTAINER_REGISTRY', 'ghcr.io/neuronsphere')}/hmd-ms-librarian:{os.environ.get('HMD_MS_LIBRARIAN_VERSION', 'stable')}",
                    "environment": {
                        "AWS_ACCESS_KEY_ID": credentials["access_key"],
                        "AWS_SECRET_ACCESS_KEY": credentials["secret_key"],
                        "AWS_SESSION_TOKEN": credentials["token"],
                        "HMD_CUSTOMER_CODE": "hmd",
                        "HMD_DID": "aaa",
                        "HMD_ENVIRONMENT": "local",
                        "HMD_REGION": "reg1",
                        "HMD_INSTANCE_NAME": repo_name,
                        "BUCKET_NAME": librarian_cfg.get("bucket_name", bucket_name),
                        "S3_ENDPOINT": s3_endpoint,
                        "CONTENT_PATH_CONFIGS": json.dumps(
                            librarian_cfg["content_item_paths"]
                        ),
                        "GRAPH_QUERY_CONFIG": json.dumps(
                            librarian_cfg.get("graph_queries", {})
                        ),
                    },
                    "depends_on": ["dynamodb", "global-graph"],
                    "volumes": [
                        f"{str(tmp_path / repo_name / 'src'/ 'cit')}:/content_item_types",
                    ],
                },
                "minio_config": {
                    "image": "quay.io/minio/minio:RELEASE.2023-04-28T18-11-17Z",
                    "entrypoint": "/bin/bash",
                    "command": "/root/minio_config.sh",
                    "volumes": [
                        f"{str(tmp_path / repo_name / 'minio_config.sh')}:/root/minio_config.sh"
                    ],
                },
            }
        }

        if not os.path.exists(tmp_path / repo_name / "src" / "docker"):
            os.mkdir(tmp_path / repo_name / "src" / "docker")

        with open(
            tmp_path / repo_name / "src" / "docker" / "docker-compose.local.yaml",
            "w",
        ) as dc:
            yaml.dump(default_docker_compose, dc)

        mickey = subprocess.run(["hmd", "mickey", "build"])

        if mickey.returncode > 0:
            logger.error(mickey.stderr)
            raise Exception("Error compiling schemas")

        pip_install = subprocess.run(["pip", "install", "-e", "src/python"])

        if pip_install.returncode > 0:
            logger.error(pip_install.stderr)
            raise Exception("Error installing schemas")

        run_local_service(repo_name, "0.0.1", [repo_name], db_init=False)


def stop():
    stop_neuronsphere()


def reload():
    start()


# TODO: Make the following method prompts more interactive to create attributes, etc.


def add_content_item_type():
    questions = {
        "short_name": {"type": "input", "required": True},
        "description": {},
        "match_regex": {},
        "mime_type": {},
    }

    data = prompt_for_values(questions, False)

    data["match_regex"] = re.compile(data["match_regex"]).pattern

    filepath = f'./src/entities/hmd_lang_librarian.content_item_types/{data["short_name"]}.cit.hmdentity'

    if os.path.exists(filepath):
        raise Exception(f"ContentItemType already exists: {filepath}")

    with open(
        filepath,
        "w",
    ) as cit:
        json.dump(data, cit, indent=2)


def add_noun():
    questions = {"name": {"required": True}}

    data = prompt_for_values(questions, False)
    namespace = os.path.basename(os.getcwd()).replace("-", "_")

    filepath = f'./src/schemas/{namespace}/{data["name"]}.hms'

    if os.path.exists(filepath):
        raise Exception(f"Noun already exists: {filepath}")

    with open(filepath, "w") as n:
        json.dump(
            {
                "namespace": namespace,
                "name": data["name"],
                "metatype": "noun",
                "attributes": {},
            },
            n,
            indent=2,
        )


def add_relationship():
    questions = {
        "name": {"required": True},
        "ref_from": {"required": True},
        "ref_to": {"required": True},
    }

    data = prompt_for_values(questions, False)
    namespace = os.path.basename(os.getcwd()).replace("-", "_")

    filepath = f'./src/schemas/{namespace}/{data["name"]}.hms'

    if os.path.exists(filepath):
        raise Exception(f"Relationship already exists: {filepath}")

    with open(filepath, "w") as n:
        json.dump(
            {
                "namespace": namespace,
                "name": data["name"],
                "ref_from": data["ref_from"],
                "ref_to": data["ref_to"],
                "metatype": "relationship",
                "attributes": {},
            },
            n,
            indent=2,
        )
