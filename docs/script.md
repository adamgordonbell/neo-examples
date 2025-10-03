
## **Pulumi Neo – Cost Optimization Script**

\[AWS Resource Explorer showing resources in us-west-2\]
 Here's the EC2 instances in my AWS account. I've got a few resources running here, but I suspect stuff I'm not using. Old volumes, unused load balancers. I'm not sure.

\[Neo prompt being typed\]
 So in Pulumi Neo I ask: *"Can you identify and remove any unused resources?"*

\[Neo analyzing infrastructure, showing resource graph\]
 Neo analyzes the infrastructure and identifies the orphaned resources—the ALB with no target groups, the unattached volume, and the unused security group.

\[Pulumi preview window with - Delete indicators\]
 It shows me a preview of what will be removed. I can verify these are safe to delete without impacting my running workloads.

\[GitHub PR diff showing resources being removed from code\]
 Neo creates a pull request so I can review exactly what's being deleted from my infrastructure as code.

\["Human in the Loop" overlay beside PR\]
 That's the crucial guardrail: I stay in control. Nothing gets deleted until I approve it.

\[GitHub Action log showing `pulumi up` with delete operations\]
 Once it's merged, my GitHub Action runs `pulumi up` and removes the unused resources.

\[AWS Resource Explorer showing fewer resources in us-west-2\]
 And back in Resource Explorer, I can see the impact—those orphaned resources are gone, saving about $200 a year.

\[Split screen: Cost before → Neo prompt → PR → Cost after\]
 In just a few minutes, Neo helped me identify waste, clean up my infrastructure, and reduce costs.

\[Pulumi Neo logo \+ pulumi.com/neo URL\]
 Pulumi Neo makes cloud cost optimization easy. Check it out today.
