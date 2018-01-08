import boto3

# ec2 = boto3.resource('ec2')
# newInstance = ec2.create_instances(ImageId=AMI_ID, MinCount=1, MaxCount=1, InstanceType=INSTANCE_TYPES['t2.micro'])
# print(newInstance[0].id)

class VPC(object):
    """Creates  Virtual Private cloud"""
    def __init__(self, cidrBlock, ipv6=False, dryRun=False, instanceTenancy='default'):
        try:
            client = boto3.client('elb')
            response = client.create_vpc(
                CidrBlock=cidrBlock,
                AmazonProvidedIpv6CidrBlock=ipv6,
                DryRun=dryRun,
                InstanceTenancy=instanceTenancy
            )
            print(response)
        except Exception as e:
            print(e)
        else:
            print("VPC creation successful")

class Instance(object):
    """ Creates an AWS EC2 Instance,USAGE: Instance((MinCount=minCount, MaxCount=maxCount, InstanceType=instanceType, ImageId=imageId))
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
    INSTANCE_TYPES = {"t2.micro": "t2.micro", "t2.medium": "t2.medium", "t2.large": "t2.large", "t2.large": "t2.large",
                      "m4.large": "m4.large", "m4.xlarge": "m4.xlarge", "m4.4xlarge": "m4.4xlarge"}
    Instances = []
    def __init__(self, minCount, maxCount, instanceType = INSTANCE_TYPES["t2.micro"], imageId = AMI_ID):
        try:
            ec2 = boto3.resource('ec2')
            self.Instances.extend(ec2.create_instances(MinCount=minCount, MaxCount=maxCount, InstanceType=instanceType, ImageId=imageId))
        except Exception as e:
            print(e)
        else:
            print("Instances created successfully.")

    def getInstances(self):
        return self.INSTANCE_TYPES

    def getAMIID(self):
        return self.AMI_ID

    def getInstances(self):
        return self.Instances

    def terminateAllInstances(self):
        try:
            for instance in self.Instances:
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

# newInstance = Instance(1, 2)
# print(newInstance.getInstances())