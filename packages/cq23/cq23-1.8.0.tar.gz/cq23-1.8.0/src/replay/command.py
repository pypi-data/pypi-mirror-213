import os
import time
import webbrowser
from multiprocessing import Process

from web_server import flask_api


def run_gui(replay_files_directory):
    gui_process = Process(target=flask_api.start, args=(replay_files_directory,))
    gui_process.start()
    webbrowser.open("https://watch.codequest.club/?base_url=localhost:2023/")
    return gui_process


def replay(*args):
    if not args:
        replays_folder = os.path.join(
            os.getcwd(), os.path.join(".game_files", "replay_files")
        )
        if not os.path.exists(replays_folder):
            print("No replay files available. You should first run a game: cq23 run")
            return
        process = run_gui(replays_folder)
        time.sleep(5 * 60)
        process.terminate()
    else:
        match_id = args[0]
        if not str(match_id).isnumeric():
            print("Match id should be a number: cq23 replay 123")
            return
        webbrowser.open(
            f"https://watch.codequest.club/?base_url=api.codequest.club/api/matches/{match_id}/"
        )
