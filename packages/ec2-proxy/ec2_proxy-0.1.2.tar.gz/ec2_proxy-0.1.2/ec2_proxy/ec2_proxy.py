"""Main module."""
import boto3
import random
from botocore.client import BaseClient
import time
import requests
from botocore.exceptions import ClientError

class TProxy():
    def __init__(self, instance_id:str = None, port:int = None, ec2:BaseClient = None) -> None:
        if not instance_id:
            raise ValueError("instance_id is required.")
        self.instance_id = instance_id
        self.port = port
        self.ec2 = ec2 or boto3.client('ec2')
        response = self.ec2.describe_instances(InstanceIds=[self.instance_id])
        try:
            self.current_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
        except KeyError:
            # Instance is likely stopped
            self.current_ip = None
        self.sg_id = response["Reservations"][0]["Instances"][0]["SecurityGroups"][0]["GroupId"]

    def shutdown(self, tries:int = 10) -> bool:
        print("Stopping the EC2 instance...")
        while True:
            try:
                self.ec2.stop_instances(InstanceIds=[self.instance_id])
            except ClientError:
                tries -= 1
                if tries == 0:
                    raise Exception("Failed to stop the EC2 instance.")
                time.sleep(10)
                continue
            else:
                break
        waiter = self.ec2.get_waiter('instance_stopped')
        waiter.wait(InstanceIds=[self.instance_id])
        print("EC2 instance stopped.")
        return True
    
    def start(self, tries:int = 10) -> str:
        # Stop the EC2 instance
        print("Starting the EC2 instance...")
        while True:
            try:
                self.ec2.start_instances(InstanceIds=[self.instance_id])
            except ClientError:
                tries -= 1
                if tries == 0:
                    raise Exception("Failed to start the EC2 instance.")
                time.sleep(10)
                continue
            else:
                break
        waiter = self.ec2.get_waiter('instance_running')
        waiter.wait(InstanceIds=[self.instance_id])
        print("EC2 instance started.")
        response = self.ec2.describe_instances(InstanceIds=[self.instance_id])
        public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
        self.current_ip = public_ip
        if self.port:
            while True:
                try:
                    requests.get(f"https://google.com", proxies={"https": f"{public_ip}:{self.port}"})
                except requests.exceptions.ConnectionError:
                    tries -= 1
                    if tries == 0:
                        raise Exception("Failed to start the proxy.")
                    time.sleep(10)
                    continue
                else:
                    break
            return public_ip + f":{self.port}"
        return public_ip 
    
    def modify_security_group(self) -> int:
        response = self.ec2.describe_security_groups(GroupIds=[self.sg_id])
        current_rules = response['SecurityGroups'][0]['IpPermissions']
        if len(current_rules) > 5:
            # Remove a port that is not 22 or 46642
            for rule in current_rules:
                if rule['FromPort'] not in [22, self.port]: # prevent removing ssh port and the port used by the proxy
                    removed_port = rule['FromPort']
                    print(f"Removing port {removed_port} from the security group...")
                    self.ec2.revoke_security_group_ingress(
                        GroupId=self.sg_id,
                        IpPermissions=[rule]
                    )
                    print(f"Port {removed_port} removed from the security group.")
                    return removed_port
        else:
            # Generate a new random port
            port = random.randint(5000, 9000)

            # Add a new inbound rule for the new port
            print(f"Opening port {port} in the security group...")
            self.ec2.authorize_security_group_ingress(
                GroupId=self.sg_id,
                IpPermissions=[
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': port,
                        'ToPort': port,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                    }
                ]
            )
            print(f"Port {port} opened in the security group.")
            return port
        
    def restart(self) -> str:
        self.shutdown()
        self.modify_security_group()
        return self.start() 
    
    def get_current_ip(self) -> str:
        response = self.ec2.describe_instances(InstanceIds=[self.instance_id])
        public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
        self.current_ip = public_ip
        return public_ip
    
