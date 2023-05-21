#!/usr/bin/env python
from constructs import Construct
from cdk8s import App, Chart
from imports import k8s
import yaml

class MyChart(Chart):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)
        
        # define resources here
        label = {"app": "cdk8s"}
        k8s.KubeDeployment(self, 'Deployment',
                                   spec=k8s.DeploymentSpec(
                replicas=2,
                selector=k8s.LabelSelector(match_labels=label),
                template=k8s.PodTemplateSpec(
                         metadata=k8s.ObjectMeta(labels=label),
                         spec=k8s.PodSpec(containers=[
                             k8s.Container(
                             name='cdk8s',
                             image='public.ecr.aws/s9u7u6x1/sample_app_001:no-db',
                             ports=[k8s.ContainerPort(container_port=80)])])))) 
                                    
                                    
                                   
                                    
                                    
                                    
                                    
                                    
                                    
                                    
        
        super().__init__(scope, f"{id}-service")
        k8s.KubeService(self, 'service',
        spec=k8s.ServiceSpec(
        type='LoadBalancer',
        ports=[k8s.ServicePort(port=80, target_port=k8s.IntOrString.from_number(80))],
        selector=label))
        

                                                                                                                        

app = App()
MyChart(app, "cdk8s")

app.synth()
