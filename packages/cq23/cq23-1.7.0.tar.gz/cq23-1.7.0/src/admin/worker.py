from main.utils import admin

from .aws import create_cq_instances, terminate_instances_by_name


def new_workers(*args):
    create_cq_instances("worker", *args)


def destroy_workers(*args):
    if (
        input("Are you sure you want to destroy all workers? (y)").lower().strip()
        != "y"
    ):
        return print("Cancelled.")
    terminate_instances_by_name("cq-worker")


@admin
def command(*args):
    if not args or args[0] not in ["new", "destroy"]:
        print("new or destroy")

    if args[0] == "new":
        new_workers(*args[1:])
    elif args[0] == "destroy":
        destroy_workers(*args[1:])
