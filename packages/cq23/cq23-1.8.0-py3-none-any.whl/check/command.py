import os
import shutil
import subprocess

import docker
from colorama import Fore
from colorama import init as color_init


def is_git_installed():
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def is_docker_installed():
    try:
        client = docker.from_env()
        client.ping()
        return True
    except (docker.errors.DockerException, docker.errors.APIError):
        return False


def has_enough_disk_space(minimum_space_gb):
    root_directory = os.path.abspath(os.sep)
    total, used, free = shutil.disk_usage(root_directory)
    free_gb = free // (2**30)  # Convert bytes to GB
    return free_gb >= minimum_space_gb


def check(*args):
    color_init(autoreset=True)
    git_installed = is_git_installed()
    docker_installed = is_docker_installed()
    enough_disk_space = has_enough_disk_space(5)

    boolean_map = {True: Fore.GREEN + "Yes", False: Fore.RED + "No"}

    print(f"Git installed: {boolean_map[git_installed]}")
    print(f"Docker installed and running: {boolean_map[docker_installed]}")
    print(f"Enough disk space: {boolean_map[enough_disk_space]}")

    if git_installed and docker_installed and enough_disk_space:
        print(Fore.LIGHTGREEN_EX + "You are all set!")
    else:
        print(Fore.YELLOW + "Some requirements are not met.")
        if not docker_installed:
            print(
                Fore.YELLOW
                + "-> If you have installed Docker Desktop, you need to make sure it's running. Search "
                "for Docker in your applications and open it. That will start Docker on your computer."
            )
