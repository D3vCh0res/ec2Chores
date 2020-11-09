import boto3
import json
from collections import OrderedDict

def askBoto():
    ec2 = boto3.client('ec2') 
    response = ec2.describe_instances()
    print(response.keys())
    print(response["Reservations"])


def display_menu():
    print("------------\tLooping\t------------")
    print("Enter 'exit' to exit, instance name 'Input' field")
    print("Enter start/stop/restart to the 'Machine State' field")

def manage_ec2_status(ec2Name, ec2State, instance_id):
    print("Asking AWS of %s to %s" % (ec2Name, ec2State))
    if ec2state == 'start':
        # Do a dryrun first to verify permissions
        try:
            ec2.start_instances(InstanceIds=[instance_id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

        # Dry run succeeded, run start_instances without dryrun
        try:
            response = ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
            print(response)
        except ClientError as e:
            print(e)
    else:
        # Do a dryrun first to verify permissions
        try:
            ec2.stop_instances(InstanceIds=[instance_id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

        # Dry run succeeded, call stop_instances without dryrun
        try:
            response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
            print(response)
        except ClientError as e:
            print(e)    

if __name__ == "__main__":
    print("------------\tec2Chore\t------------")
    machines = {}
    ec2 = boto3.client('ec2') 
    describeResponse = ec2.describe_instances()
    instances = describeResponse["Reservations"][0]["Instances"]
    
    print("\nMapping Instances...")
    for instance in instances:
        tags = instance["Tag"]
        for tag in tags:
            if tag["Key"] == "Name":
                machine_name = tag["Value"]

        machines[machine_name] = instance["InstanceId"]
    
    # To the user
    while True:
        display_menu()
        ec2Name = input("\nEC2 Name: ")
        if ec2Name == "exit":
            break
        else:
            ec2State = input("\nMachine State: ")
            manage_ec2_status(ec2Name, ec2State, machines[ec2Name])
        print("\n...Back to you\n")
    print("\n*****\tDone\t*****")