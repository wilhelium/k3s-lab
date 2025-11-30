#!/usr/bin/env python
from constructs import Construct
from cdk8s import App, Chart
from imports import k8s


class MyChart(Chart):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        label = {"app": "homeassistant"}

        k8s.KubeDeployment(
            self,
            "app",
            spec=k8s.DeploymentSpec(
                replicas=2,
                selector=k8s.LabelSelector(match_labels=label),
                template=k8s.PodTemplateSpec(
                    metadata=k8s.ObjectMeta(labels=label),
                    spec=k8s.PodSpec(
                        containers=[
                            k8s.Container(
                                name="app-container",
                                image="homeassistant/home-assistant:sha256:88d08b12c87838955af7329040803f16a19f3ef62015300a7e1f894785e78883",
                                ports=[k8s.ContainerPort(container_port=443)],
                                volume_mounts=[
                                    k8s.VolumeMount(
                                        mount_path="/config", name="automation_config"
                                    )
                                ],
                            )
                        ]
                    ),
                ),
            ),
        )
        k8s.KubeService(
            self,
            "service",
            spec=k8s.ServiceSpec(
                type="LoadBalancer",
                ports=[k8s.ServicePort(port=10443, name="HTTPS Access", node_port=443)],
                selector=label,
            ),
        )


app = App()
MyChart(app, "homeassistant")

app.synth()
