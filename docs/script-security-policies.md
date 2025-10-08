
## **Pulumi Neo – Security Policy Enforcement Script**

\[AWS Console showing security groups in ca-central-1\]
Here are the security groups in my AWS account. I've got infrastructure running, but I'm not sure if everything follows our security best practices.

\[Pulumi Policy Pack configuration visible\]
We've set up Pulumi Policy as Code to automatically enforce security compliance. One of our mandatory policies prohibits SSH and RDP access from the internet.

\[Terminal showing `pulumi preview` with policy violation\]
When I run `pulumi preview`, the policy pack catches a violation: a bastion security group allows SSH from 0.0.0.0/0—that's the entire internet.

\[Policy violation message highlighted\]
The error message is clear: *"Security group 'bastion-sg' allows SSH (port 22) access from the internet (0.0.0.0/0). This is a security risk. Restrict access to specific IP addresses or remove this rule."*

\[Neo prompt being typed\]
So I ask Pulumi Neo: *"Fix the security group policy violations"*

\[Neo analyzing the policy output\]
Neo reads the policy violation, understands the issue, and proposes a fix: restrict SSH access to a specific trusted IP range instead of the entire internet.

\[Code diff showing security group ingress rule change\]
It updates the infrastructure code, changing the CIDR block from `0.0.0.0/0` to a specific IP range like `203.0.113.0/24`.

\[Terminal showing `pulumi preview` passing policy checks\]
When Neo runs preview again, the policy checks pass. No violations. The infrastructure is now compliant.

\[GitHub PR showing the security fix\]
Neo creates a pull request with the security fix. I can review the exact change before it's deployed.

\["Policy-Driven Security" overlay\]
This is Policy as Code in action: automated enforcement of security best practices, with AI that can understand and fix violations.

\[GitHub Action log showing successful deployment with policy checks\]
Once merged, the GitHub Action deploys the fix. The policy pack runs automatically on every deployment, ensuring we stay compliant.

\[Split screen: Before (0.0.0.0/0) → Neo → PR → After (specific CIDR)\]
In minutes, Neo identified the security risk, proposed a compliant fix, and helped us close a potential attack vector.

\[Pulumi Neo logo \+ pulumi.com/neo URL\]
Pulumi Neo makes security compliance effortless. Try it today.
