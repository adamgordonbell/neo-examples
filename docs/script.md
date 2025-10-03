
## **Pulumi Neo – Kubernetes Scaling Script (Polished)**

\[k9s `:nodes` showing 2 nodes\]  
 Hey, here’s my Kubernetes cluster running on AWS. Right now it’s just two nodes, but I want to pre-scale it before a workload—I’ve got some training runs coming up.

\[Neo prompt being typed\]  
 So in Pulumi Neo I ask: *“Can you add a new node group?”*

\[Neo output showing new node group resource\]  
 Neo understands the request and generates the Pulumi code for that new group.

\[Pulumi preview window with ✓ Create indicators\]  
 It shows me a preview—and we can see this is just an addition, nothing destructive. A safe change.

\[GitHub PR diff with new node group\]  
 Neo creates a pull request so I can review exactly what’s being added.

\[“Human in the Loop” overlay beside PR\]  
 That’s the crucial guardrail: I stay in control, so nothing Neo does can accidentally take down prod.

\[GitHub Action log showing `pulumi up`\]  
 Once it’s merged, my GitHub Action runs `pulumi up` and applies the change.

\[k9s `:nodes` now showing 4 nodes, burst label highlighted\]  
 And back in Kubernetes, I can see the new nodes have joined the cluster.

\[Split screen: Neo prompt → PR → k9s nodes\]  
 In under a minute, I’ve gone from a natural language request to scaled-up capacity in my cluster.

\[Pulumi Neo logo \+ pulumi.com/neo URL\]  
 Pulumi Neo makes it easy to manage Kubernetes at scale. Check it out today.
