import boto3


class Instance(object):
    """ Creates an AWS EC2 Instance,
    USAGE: Instance((MinCount=minCount, MaxCount=maxCount, InstanceType=instanceType, ImageId=imageId))
        For the created Instance list use getInstances()
        For the types of Available instances use getInstanceTypes()"""
    # AMI: AMAZON MACHINE IMAGE
    # AMI TYPE: UBUNTU SERVER 16.04 LTS
    AMI_ID = "ami-f3e5aa9c"

    # T2,M4: BASIC GENERAL PURPOSE MACHINES
    # INSTANCE TYPE-CPU VIRTUAL CORES-RAM
    # T2 MICRO-1-1
    # T2 MEDUIM-2-4
    # T2 LARGE-2-8
    # M4 LARGE-2-8
    # M4 XLARGE-4-16
    # M4 4X LARGE-16-64
    INSTANCE_TYPES = {"t2.micro": "t2.micro", "t2.medium": "t2.medium", "t2.large": "t2.large",
                      "m4.large": "m4.large", "m4.xlarge": "m4.xlarge", "m4.4xlarge": "m4.4xlarge"}

    def __init__(self, ec2, image_id=AMI_ID, instance_type=INSTANCE_TYPES["t2.micro"],
                 max_count=1, min_count=1, security_group=[]):
        try:
            instances = ec2.create_instances(
                    ImageId=image_id, InstanceType=instance_type, MaxCount=max_count, MinCount=min_count,
                    NetworkInterfaces=security_group)
            instances[0].wait_until_running()
            print(instances[0].id)
            self.instances = instances
        except Exception as e:
            print(e)
        else:
            print("Instances created successfully.")

    def getAMIID(self):
        return self.AMI_ID

    def getInstances(self):
        return self.Instances

    def terminateAllInstances(self, instances):
        try:
            for instance in instances:
                response = instance.terminate()
                print (response)
        except Exception as e:
            print(e)
        else:
            print("Instance deletion successful")

class LoadBalancer(object):
    """Creates an AWS EC2 Load balancer instance
    """
    def __init__(self, loadBalancerName, listeners, securityGroups):
        client = boto3.client('elb')
        response = client.create_load_balancer(
            LoadBalancerName=loadBalancerName,
            Listeners=listeners,
            Subnets=[
                'string',
            ],
            SecurityGroups=securityGroups,
            Scheme='string',
            Tags=[
                {
                    'Key': 'string',
                    'Value': 'string'
                },
            ]
        )
        print(response)

def createVpc(ec2):
    vpc = ec2.create_vpc()  # FIXME
    vpc.create_tags()  # FIXME
    vpc.wait_untill_available()
    return vpc

def createRoute(routeTable, internetGateway):
    return routeTable.create_route(
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=internetGateway.id
    )


ec2 = boto3.resource('ec2')
#Create VPC
vpc = createVpc(ec2)
print(vpc.id)

#Create Gateway and attach to VPC
internetGateway = ec2.create_internet_gateway()
vpc.attach_internet_gateway(InternetGatewayId=internetGateway.id)

#Creating a routeTable and public route
routeTable = vpc.create_route_table()
route = createRoute(routeTable, internetGateway)
print(routeTable.id)

# Create Subnet
subnet = ec2.create_subnet(CidrBlock='192.168.1.0/24', VpcId=vpc.id)
print(subnet.id)

# Associate the route table with the subnet
routeTable.associate_with_subnet(SubnetId=subnet.id)

# Create security group
securityGroup = ec2.create_security_group(
    GroupName='', Description='', VpcId=vpc.id)
securityGroup.authorize_ingress(
    CidrIp='0.0.0.0/0',
    IpProtocol='icmp',
    FromPort=-1,
    ToPort=-1
)
print(securityGroup.id)

# Create instance
newInstances = Instance(ec2, None, None, 1, 1,[{'SubnetId': subnet.id, 'DeviceIndex': 0, 'AssociatePublicIpAddress': False, 'Groups': [securityGroup.group_id]}])
