import json
import os
import subprocess
import sys
import webbrowser
from multiprocessing import Process

from web_server import flask_api

from . import docker_tools

MATCH_TIMEOUT_SECONDS = 12 * 60  # This should ideally match the one in game worker


def run_gui():
    replay_files_directory = os.path.join(os.getcwd(), "replay_files")
    # gui_directory = os.path.join(os.getcwd(), "gui")
    gui_process = Process(target=flask_api.start, args=(replay_files_directory,))
    gui_process.start()
    # webbrowser.open("file://" + os.path.join(gui_directory, "index.html"))
    webbrowser.open("https://watch.codequest.club/?base_url=localhost:2023/")
    return gui_process


def stop_gui(gui_process):
    func = os.environ.get("werkzeug.server.shutdown")
    if func is None:
        print("Can't stop gracefully, killing the server process.")
        gui_process.terminate()
    else:
        func()
        gui_process.join(timeout=5)
        if gui_process.is_alive():
            gui_process.terminate()


def run_gcs(gcs_folder_name, game_map=None):
    gcs_src_dir = os.path.join(gcs_folder_name, "src")
    clients_file_content = [
        {
            "id": "1",
            "name": "Your Code - 1",
            "image": docker_tools.get_client_image_tag(),
        },
        {
            "id": "2",
            "name": "Your Code - 2",
            "image": docker_tools.get_client_image_tag(),
        },
    ]
    clients_file_address = "clients.json"

    with open(os.path.join(gcs_src_dir, clients_file_address), "w") as f:
        f.write(json.dumps(clients_file_content))

    subprocess_args = [
        sys.executable,
        "controller.py",
        docker_tools.get_server_image_tag(),
        clients_file_address,
    ]

    if game_map:
        subprocess_args.append("--server-arg")
        subprocess_args.append("-m " + str(game_map))

    print("Starting the game interface...")
    gui_process = run_gui()

    print("Starting the game...")
    subprocess.run(subprocess_args, timeout=MATCH_TIMEOUT_SECONDS, cwd=gcs_src_dir)
    print("Game finished.")

    print("Stopping the game interface...")
    stop_gui(gui_process)

    os.remove(os.path.join(gcs_src_dir, clients_file_address))
