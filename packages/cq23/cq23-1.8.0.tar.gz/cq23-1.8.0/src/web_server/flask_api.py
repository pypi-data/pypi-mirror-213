import os.path

from flask import Flask, jsonify, request, send_file

app = Flask(__name__)
ROOT_DIRECTORY = None
PORT = None


def get_full_path_or_404(file_name):
    full_file_path = os.path.join(ROOT_DIRECTORY, file_name)
    print(full_file_path)
    if not os.path.exists(full_file_path):
        return False, (jsonify({"message": "Replay file not found."}), 404)

    return True, full_file_path


@app.route("/", methods=["GET"])
def heartbeat():
    return "I'm up"


@app.route("/download_file", methods=["GET"])
def download_file():
    assert ROOT_DIRECTORY
    file_name = request.args["file_name"]
    valid, response = get_full_path_or_404(file_name)
    if not valid:
        return response
    return send_file(response)


@app.route("/get_replay_file_url", methods=["GET"])
def get_file_url():
    assert ROOT_DIRECTORY and PORT
    file_name = request.args["file_name"]

    valid, response = get_full_path_or_404(file_name)
    if not valid:
        return response

    return jsonify(
        {
            "message": "ok",
            "url": f"http://127.0.0.1:{PORT}/download_file?file_name={file_name}",
        }
    )


@app.route("/get_replay_file_content", methods=["GET"])
def get_file_contents():
    assert ROOT_DIRECTORY
    file_name = request.args["file_name"]

    valid, response = get_full_path_or_404(file_name)
    if not valid:
        return response

    with open(response) as f:
        file_content = f.read()

    return jsonify({"message": "ok", "content": file_content})


def start(replay_files_directory, port=2023, debug=False):
    global ROOT_DIRECTORY, PORT
    ROOT_DIRECTORY = replay_files_directory
    PORT = port

    app.run(debug=debug, port=PORT, threaded=True)
