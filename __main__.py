"""EKS cluster with custom networking and single node group"""

import pulumi
import pulumi_aws as aws
import pulumi_eks as eks
import pulumi_kubernetes as k8s

# -----------------------------
# Networking (simple & public)
# -----------------------------
vpc = aws.ec2.Vpc(
    "eks-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={"Name": "eks-vpc"},
)

igw = aws.ec2.InternetGateway(
    "eks-igw",
    vpc_id=vpc.id,
    tags={"Name": "eks-igw"},
)

public_subnet_1 = aws.ec2.Subnet(
    "public-subnet-1",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone="ca-central-1a",
    map_public_ip_on_launch=True,
    tags={
        "Name": "public-subnet-1",
        "kubernetes.io/role/elb": "1",
    },
)

public_subnet_2 = aws.ec2.Subnet(
    "public-subnet-2",
    vpc_id=vpc.id,
    cidr_block="10.0.2.0/24",
    availability_zone="ca-central-1b",
    map_public_ip_on_launch=True,
    tags={
        "Name": "public-subnet-2",
        "kubernetes.io/role/elb": "1",
    },
)

public_rt = aws.ec2.RouteTable(
    "public-rt",
    vpc_id=vpc.id,
    routes=[aws.ec2.RouteTableRouteArgs(cidr_block="0.0.0.0/0", gateway_id=igw.id)],
    tags={"Name": "public-rt"},
)

aws.ec2.RouteTableAssociation(
    "public-rta-1",
    subnet_id=public_subnet_1.id,
    route_table_id=public_rt.id,
)
aws.ec2.RouteTableAssociation(
    "public-rta-2",
    subnet_id=public_subnet_2.id,
    route_table_id=public_rt.id,
)

subnet_ids = [public_subnet_1.id, public_subnet_2.id]

# -----------------------------
# IAM Role for Node Groups
# -----------------------------
node_role = aws.iam.Role(
    "eks-node-role",
    assume_role_policy="""{
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "ec2.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }""",
)

# Attach required policies for EKS worker nodes
aws.iam.RolePolicyAttachment(
    "eks-node-policy",
    role=node_role.name,
    policy_arn="arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy",
)

aws.iam.RolePolicyAttachment(
    "eks-cni-policy",
    role=node_role.name,
    policy_arn="arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy",
)

aws.iam.RolePolicyAttachment(
    "eks-ecr-policy",
    role=node_role.name,
    policy_arn="arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly",
)

# Create instance profile for the node role
node_instance_profile = aws.iam.InstanceProfile(
    "eks-node-instance-profile",
    role=node_role.name,
)

# -----------------------------
# EKS Control Plane
# -----------------------------
cluster = eks.Cluster(
    "eks-cluster",
    vpc_id=vpc.id,
    subnet_ids=subnet_ids,
    skip_default_node_group=True,  # we'll add our own managed node group
    create_oidc_provider=True,     # helpful for IRSA / add-ons later
    # CRITICAL: Use API auth mode to avoid aws-auth ConfigMap bootstrap issues
    # Note: instance_roles is not supported with API auth mode - roles are
    # registered automatically via access entries instead
    authentication_mode=eks.AuthenticationMode.API,
    # Disable managed CoreDNS add-on to avoid its (sometimes slow) lifecycle
    coredns_addon_options=eks.CoreDnsAddonOptionsArgs(enabled=False),
    tags={"Name": "eks-cluster", "Environment": "development"},
)

# -----------------------------
# Managed Node Group
# -----------------------------
# Single node group: keeps kube-system (CoreDNS, CNI, etc.) instantly available
system_ng = eks.ManagedNodeGroup(
    "mng-system",
    cluster=cluster,
    instance_types=["t3.small"],
    node_role=node_role,
    subnet_ids=subnet_ids,
    scaling_config=aws.eks.NodeGroupScalingConfigArgs(
        min_size=1,
        desired_size=1,
        max_size=2,
    ),
    ami_type="AL2023_x86_64_STANDARD",
)

# -----------------------------
# Kubernetes Workload (to show cluster is in use)
# -----------------------------
k8s_provider = k8s.Provider(
    "k8s-provider",
    kubeconfig=cluster.kubeconfig,
)

# Simple nginx deployment to demonstrate cluster is actively used
nginx_deployment = k8s.apps.v1.Deployment(
    "nginx-demo",
    metadata=k8s.meta.v1.ObjectMetaArgs(
        name="nginx-demo",
        namespace="default",
    ),
    spec=k8s.apps.v1.DeploymentSpecArgs(
        replicas=1,
        selector=k8s.meta.v1.LabelSelectorArgs(
            match_labels={"app": "nginx"},
        ),
        template=k8s.core.v1.PodTemplateSpecArgs(
            metadata=k8s.meta.v1.ObjectMetaArgs(
                labels={"app": "nginx"},
            ),
            spec=k8s.core.v1.PodSpecArgs(
                containers=[
                    k8s.core.v1.ContainerArgs(
                        name="nginx",
                        image="nginx:alpine",
                        resources=k8s.core.v1.ResourceRequirementsArgs(
                            requests={
                                "cpu": "100m",
                                "memory": "64Mi",
                            },
                            limits={
                                "cpu": "200m",
                                "memory": "128Mi",
                            },
                        ),
                    )
                ],
            ),
        ),
    ),
    opts=pulumi.ResourceOptions(provider=k8s_provider, depends_on=[system_ng]),
)

# -----------------------------
# Unused Resources (to be identified and removed)
# -----------------------------

# Unused security group - not referenced by any resource
unused_sg = aws.ec2.SecurityGroup(
    "unused-security-group",
    vpc_id=vpc.id,
    description="Old security group from a deleted application - no longer needed",
    tags={"Name": "unused-sg", "Note": "Created for test app that was removed"},
)

# Unused Application Load Balancer - no target groups, no listeners
unused_alb = aws.lb.LoadBalancer(
    "unused-alb",
    internal=False,
    load_balancer_type="application",
    security_groups=[unused_sg.id],
    subnets=[public_subnet_1.id, public_subnet_2.id],
    tags={"Name": "unused-alb", "Note": "Created for ingress testing - never configured"},
)

# Unattached EBS volume - orphaned from a deleted workload
unused_volume = aws.ebs.Volume(
    "unused-ebs-volume",
    availability_zone="ca-central-1a",
    size=10,
    type="gp3",
    tags={"Name": "unused-volume", "Note": "Detached from deleted pod, no longer needed"},
)

# -----------------------------
# Exports
# -----------------------------
pulumi.export("cluster_name", cluster.eks_cluster.name)
pulumi.export("kubeconfig", cluster.kubeconfig)
pulumi.export("vpc_id", vpc.id)
pulumi.export("region", "ca-central-1")
