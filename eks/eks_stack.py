from aws_cdk import Stack
from aws_cdk import aws_iam as iam
from aws_cdk import aws_eks as eks
from aws_cdk import aws_ec2 as ec2
import yaml
from aws_cdk.lambda_layer_kubectl_v25 import KubectlV25Layer

class ClusterStack(Stack):

    def __init__(self, scope, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Look up the default VPC
        vpc = ec2.Vpc.from_lookup(self, id="VPC", is_default=True)

        # Create master role for EKS Cluster
        iam_role = iam.Role(self, id=f"{construct_id}-iam",
                            role_name=f"{construct_id}-iam", assumed_by=iam.AccountRootPrincipal())

        kubectl_layer = KubectlV25Layer(self, "helm-cdk-layer")

        # Creating Cluster with EKS
        eks_cluster = eks.Cluster(
            self, id=f"{construct_id}-cluster", 
            cluster_name=f"{construct_id}-cluster", 
            masters_role=iam_role, 
            kubectl_layer=kubectl_layer,
            default_capacity_instance=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO), 
            default_capacity=2,
            version=eks.KubernetesVersion.V1_25,
            default_capacity_type=eks.DefaultCapacityType.NODEGROUP
        )

        
# Read the deployment config
        with open("./cdk8s/dist/cdk8s.k8s.yaml", 'r') as stream:
              deployment_yaml = yaml.load(stream, Loader=yaml.FullLoader)

        # Read the service config
        with open("./cdk8s/dist/cdk8s-service.k8s.yaml", 'r') as stream:
              service_yaml = yaml.load(stream, Loader=yaml.FullLoader)

        eks_cluster.add_manifest("f{construct_id}-app-deployment", deployment_yaml)
        eks_cluster.add_manifest("f{construct_id}-app-service", service_yaml)

        

        eks.HelmChart(self, "helmrepo",
                      cluster=eks_cluster,
                      chart="flux",
                      repository="https://charts.fluxcd.io",
                      release="flux",
                      values= {
                           'git.url':'git@github.com\:org/repo'
                      })
        # eks_cluster.add_helm_chart(
        