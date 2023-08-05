import hashlib
import re
import typer
import os
import sys
import requests
import zipfile
import tempfile
import yaspin
import time
from termcolor import colored
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper
from cerebrium import __version__ as cerebrium_version

app = typer.Typer()
env = os.getenv("ENV", "prod")

dashboard_url = (
    "https://dashboard.cerebrium.ai"
    if env == "prod"
    else "https://dev-dashboard.cerebrium.ai"
)
api_url = (
    "https://dev-rest-api.cerebrium.ai"
    if env == "dev"
    else "https://rest-api.cerebrium.ai"
)


@app.command()
def version():
    """
    Print the version of the Cerebrium CLI
    """
    print(cerebrium_version)


@app.command()
def login(
    private_api_key: str = typer.Argument(
        ...,
        help="Private API key for the user. Sets the environment variable CEREBRIUM_API_KEY.",
    )
):
    """
    Set private API key for the user as an environment variable
    """
    os.environ["CEREBRIUM_API_KEY"] = private_api_key


@app.command()
def deploy(
    name: str = typer.Argument(..., help="Name of the builder deployment."),
    api_key: str = typer.Argument(
        ..., envvar="CEREBRIUM_API_KEY", help="Private API key for the user."
    ),
    hardware: str = typer.Option(
        "GPU",
        help="Hardware to use for the builder deployment. Can be one of 'CPU', 'GPU' or 'A10'.",
    ),
    init_debug: bool = typer.Option(
        False,
        help="Stops the container after initialization.",
    ),
    pre_init_debug: bool = typer.Option(
        False,
        help="Stops the container before initialization.",
    ),
    log_level: str = typer.Option(
        "INFO",
        help="Log level for the builder deployment. Can be one of 'DEBUG' or 'INFO'",
    ),
):
    """
    Deploy a builder deployment to Cerebrium
    """
    print(f"Deploying {name} with {hardware} hardware to Cerebrium...")

    requirements_hash = "REQUIREMENTS_FILE_DOESNT_EXIST"
    pkglist_hash = "PKGLIST_FILE_DOESNT_EXIST"

    # Calc MD5 hash of ./requirements.txt
    if os.path.exists("./requirements.txt"):
        with open("./requirements.txt", "rb") as f:
            requirements_hash = hashlib.md5(f.read()).hexdigest()

    # Calc MD5 hash of ./pkglist.txt if it exists
    if os.path.exists("./pkglist.txt"):
        with open("./pkglist.txt", "rb") as f:
            pkglist_hash = hashlib.md5(f.read()).hexdigest()

    # Hit the deploy endpoint to get the upload URL
    upload_url_response = requests.post(
        f"{api_url}/deploy",
        headers={"Authorization": api_key},
        json={
            "name": name,
            "hardware": hardware.upper(),
            "init_debug": init_debug,
            "pre_init_debug": pre_init_debug,
            "log_level": log_level.upper(),
            "cerebrium_version": cerebrium_version,
            "requirements_hash": requirements_hash,
            "pkglist_hash": pkglist_hash,
        },
    )
    if upload_url_response.status_code != 200:
        print("API request failed with status code:", upload_url_response.status_code)
        print("Error getting upload URL:", upload_url_response.text)
        upload_url_response.raise_for_status()

    upload_url = upload_url_response.json()["uploadUrl"]
    project_id = upload_url_response.json()["projectId"]
    zip_file_name = upload_url_response.json()["keyName"]
    endpoint = upload_url_response.json()["internalEndpoint"]
    build_id = upload_url_response.json()["buildId"]

    print(f"Build ID: {build_id}")

    # Zip all files in the current directory and upload to S3
    print("Zipping files...")
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, zip_file_name)
        dir_name = os.path.dirname(zip_path)
        os.makedirs(dir_name, exist_ok=True)
        with zipfile.ZipFile(zip_path, "w") as zip_file:
            # write every file in the current directory and subdirectories to the zip file
            for root, dirs, files in os.walk("."):
                for file in files:
                    if file != zip_file_name and file.lower() not in (
                        "secrets.json",
                        "secrets.yaml",
                        "secrets.yml",
                    ):
                        zip_file.write(os.path.join(root, file))
        print("⬆️  Uploading to Cerebrium...")
        with open(zip_path, "rb") as f:
            headers = {
                "Content-Type": "application/zip",
            }
            with tqdm(
                total=os.path.getsize(zip_path),
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                colour="#EB3A6F",
            ) as pbar:  # type: ignore
                wrapped_f = CallbackIOWrapper(pbar.update, f, "read")
                upload_response = requests.put(
                    upload_url,
                    headers=headers,
                    data=wrapped_f,  # type: ignore
                    timeout=60,
                    stream=True,
                )
            if upload_response.status_code != 200:
                print(
                    "API request failed with status code:", upload_response.status_code
                )
                print("Error uploading to Cerebrium:", upload_response.text)
                sys.exit(1)
            else:
                print("✅ Resources uploaded successfully.")

    # Poll the streamBuildLogs endpoint with yaspin for max of 10 minutes to get the build status
    t1 = time.time()
    seen_index = 0
    with yaspin.yaspin(text="🔨 Building...", color="yellow") as spinner:
        build_status = "IN_PROGRESS"
        while build_status != "success":
            build_status_response = requests.get(
                f"{api_url}/streamBuildLogs",
                params={"buildId": build_id},
                headers={"Authorization": api_key},
            )
            if build_status_response.status_code != 200:
                print(
                    "API request failed with status code:",
                    build_status_response.status_code,
                )
                print("Error getting build status:", build_status_response.text)
                sys.exit(1)
            else:
                build_status = build_status_response.json()["status"]
                response_logs = build_status_response.json()["logs"]
                if response_logs:
                    concat_logs = "".join(response_logs)
                    logs = concat_logs.split("\n")[:-1]
                else:
                    continue

                for message in logs[seen_index:]:
                    if message:
                        match = re.match(
                            r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{9})Z ", message
                        )
                        if (
                            match is not None
                        ):  # If the regex matches the beginning of the string
                            created = match.group(
                                1
                            )  # The first group is the creation time
                            message = message[len(created) + 2 :]
                        spinner.write(f"{message}")
                    else:
                        spinner.write("\n")
                seen_index = len(logs)
                spinner.text = f"🔨 Building... Status: {build_status}"
                time.sleep(1)
            if time.time() - t1 > 600:
                spinner.fail("⏲️ Build timed out.")
                sys.exit(1)
            elif build_status == "build_failure" or build_status == "init_failure":
                spinner.fail("❌ Build failed.")
                sys.exit(1)
        spinner.text = f"Status: {build_status}"
        spinner.ok("🚀 Build complete!")
        print("\n🌍 Endpoint:", endpoint, "\n")
        print("💡 You can call the endpoint with the following curl command:")
        print(
            colored(
                f"curl -X POST {endpoint} \\\n"
                "     -H 'Content-Type: application/json' \\\n"
                "     -H 'Authorization: <public_api_key>' \\\n"
                "     --data '{}'",
                "green",
            )
        )
        print("----------------------------------------")
        print(
            f"🔗 View builds: {dashboard_url}/projects/{project_id}/models/{project_id}-{name}?tab=builds"
        )
        print(
            f"🔗 View runs: {dashboard_url}/projects/{project_id}/models/{project_id}-{name}?tab=runs"
        )


if __name__ == "__main__":
    app()
