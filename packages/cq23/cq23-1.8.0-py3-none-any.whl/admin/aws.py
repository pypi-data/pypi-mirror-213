import os
import subprocess
import time

import boto3


def create_ec2_instance(
    volume_size,
    iam_role_arn,
    ami_id,
    sg_id,
    instance_name,
    instance_type="t2.small",
    key_name="aws5-ap-southeast-2",
):
    ec2 = boto3.client("ec2")

    # Create a new EC2 instance
    response = ec2.run_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        MinCount=1,
        MaxCount=1,
        BlockDeviceMappings=[
            {"DeviceName": "/dev/sda1", "Ebs": {"VolumeSize": volume_size}}
        ],
        IamInstanceProfile={"Arn": iam_role_arn},
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [{"Key": "Name", "Value": instance_name}],
            }
        ],
        KeyName=key_name,
        SecurityGroupIds=[sg_id],
    )

    # Extract the instance ID and IP address
    instance_id = response["Instances"][0]["InstanceId"]

    # Describe the instance to get the public IP address
    time.sleep(1)
    describe_response = ec2.describe_instances(InstanceIds=[instance_id])
    instance_ip = describe_response["Reservations"][0]["Instances"][0].get(
        "PublicIpAddress"
    )

    print("-------------------------------------------")
    print(f"Created EC2 instance with ID: {instance_id}")
    print(f"Public IP address: {instance_ip}")

    return instance_id, instance_ip


def check_ssh_readiness(instance_id):
    ec2 = boto3.client("ec2")

    while True:
        response = ec2.describe_instance_status(
            InstanceIds=[instance_id], IncludeAllInstances=True
        )
        instance_status = response["InstanceStatuses"]

        if not instance_status:
            print(f"No instance found with ID: {instance_id}")
            return False

        state = instance_status[0]["InstanceState"]["Name"]
        status = instance_status[0]["InstanceStatus"]["Status"]

        if state == "running" and status == "ok":
            print(
                f"Instance {instance_id} is running and ready to accept SSH connections."
            )
            return True
        elif state == "terminated":
            print(f"Instance {instance_id} is terminated.")
            return False

        print(
            f"Instance {instance_id} is not yet ready. Current state: {state}. Status: {status}"
        )
        print("Waiting...")
        time.sleep(10)


def terminate_instances_by_name(name):
    ec2 = boto3.client("ec2")

    response = ec2.describe_instances(
        Filters=[
            {"Name": "tag:Name", "Values": [name]},
            {"Name": "instance-state-name", "Values": ["running"]},
        ]
    )

    instance_ids = []
    reservations = response["Reservations"]

    if not reservations:
        print(f"No instances found with the name: {name}")
        return

    for reservation in reservations:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            instance_ids.append(instance_id)

    if not instance_ids:
        print(f"No instances found with the name: {name}")
        return

    response = ec2.terminate_instances(InstanceIds=instance_ids)

    if "TerminatingInstances" in response:
        print("Terminating the following instances:")
        for instance in response["TerminatingInstances"]:
            print(f"- {instance['InstanceId']}")
    else:
        print("No instances terminated.")


def create_cq_instances(instance_type, *args):
    assert instance_type in ["worker", "builder"]

    ami_id = "ami-05f998315cca9bfe3"
    role_arn = os.getenv("CQ23CLI_IAM_ROLE_ARN")
    if not role_arn:
        return print("Role ARN is needed for creating new instances.")
    sg_id = os.getenv("CQ23CLI_SG_ID")
    if not sg_id:
        return print("SG ID is needed for creating new instances.")
    if not args or not str(args[0]).isnumeric():
        return print("Invalid number of instances:", args[0])

    instance_count = int(args[0])
    instance_ids = []
    instance_ips = []
    for i in range(instance_count):
        i_id, i_ip = create_ec2_instance(
            20, role_arn, ami_id, sg_id, f"cq-{instance_type}", "t2.small"
        )
        instance_ids.append(i_id)
        instance_ips.append(i_ip)

    time.sleep(5)

    for i in range(len(instance_ips)):
        if not check_ssh_readiness(instance_ids[i]):
            print("Failed!")
            continue
        subprocess.run(["make", "deploy", f"ip={instance_ips[i]}"], check=True)

    print(f"All {instance_type}s built and deployed.")
    print("\n".join(instance_ips))
