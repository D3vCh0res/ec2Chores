import sys
import boto3
import json
from collections import OrderedDict
from botocore.exceptions import ClientError

ec2_pem_location = ""

def stopInstance(instance):
    # Do a dryrun first to verify permissions
    try:
        #print("Dry run - stop")
        response = instance.stop( DryRun=True, Force=True )
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise
    try:
        print("Actual run - stop")
        response = instance.stop( DryRun=False, Force=True )
        #print(response)
        print("waiting to be stopped ...")
        instance.wait_until_stopped()
        print("Stopped Instance")
    except ClientError as e:
        print(e)      

def startInstance(instance):
    # Do a dryrun first to verify permissions
    try:
        #print("Dry run - start")
        response = instance.start(AdditionalInfo='string', DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise
    try:
        print("Actual run - start")
        response = instance.start(AdditionalInfo='string', DryRun=False)
        #print(response)
        print("waiting to be running ...")
        instance.wait_until_running()
        print("Started Instance")
        instance_ip = instance.public_ip_address
        print("public_ip: " + instance_ip)
    except ClientError as e:
        print(e)   

if __name__ == "__main__":
    state = sys.argv[1]
    ec2Name = sys.argv[2]
    print("------------\tec2Chore\t------------")
    instance_id = ""
    ec2 = boto3.client('ec2') 
    describeResponse = ec2.describe_instances()
    instances = describeResponse["Reservations"][0]["Instances"]
    for instance in instances:
        for tag in instance["Tags"]:
            if tag["Key"] == "Name":
                if tag["Value"] == ec2Name:
                    instance_id = instance["InstanceId"]
    if instance_id == "":
        print(" Instance '%s' not found" % (ec2Name))
    else:
        ec2_resource = boto3.resource('ec2')
        instance = ec2_resource.Instance(instance_id)
        if state.lower() == "start":
            startInstance(instance)
        elif state.lower() == "stop":
            stopInstance(instance)
        else:
            print("Invalid Option")
    
