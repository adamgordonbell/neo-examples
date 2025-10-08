import * as policy from "@pulumi/policy";

new policy.PolicyPack("aws-security-policies", {
    policies: [
        // Resource-level policy: runs when resources are being created/modified
        {
            name: "prohibit-public-ssh-rdp-resource",
            description: "Prohibits security groups from allowing SSH (22) or RDP (3389) access from the internet (0.0.0.0/0).",
            enforcementLevel: "mandatory",
            validateResource: (args, reportViolation) => {
                if (args.type !== "aws:ec2/securityGroup:SecurityGroup") {
                    return;
                }

                const ingress = args.props.ingress || [];

                for (const rule of ingress) {
                    const cidrBlocks = rule.cidrBlocks || [];
                    const fromPort = rule.fromPort;
                    const toPort = rule.toPort;

                    // Check if rule allows access from 0.0.0.0/0
                    const allowsPublicAccess = cidrBlocks.some(
                        (cidr: string) => cidr === "0.0.0.0/0"
                    );

                    if (allowsPublicAccess) {
                        // Check if SSH (22) or RDP (3389) ports are exposed
                        const exposesSSH = fromPort !== undefined && toPort !== undefined &&
                            fromPort <= 22 && toPort >= 22;
                        const exposesRDP = fromPort !== undefined && toPort !== undefined &&
                            fromPort <= 3389 && toPort >= 3389;

                        if (exposesSSH) {
                            reportViolation(
                                `Security group '${args.name}' allows SSH (port 22) access from the internet (0.0.0.0/0). ` +
                                `This is a security risk. Restrict access to specific IP addresses or remove this rule.`
                            );
                        }

                        if (exposesRDP) {
                            reportViolation(
                                `Security group '${args.name}' allows RDP (port 3389) access from the internet (0.0.0.0/0). ` +
                                `This is a security risk. Restrict access to specific IP addresses or remove this rule.`
                            );
                        }
                    }
                }
            },
        },
        // Stack-level policy: runs on every preview/up, checks ALL resources including already-deployed ones
        {
            name: "prohibit-public-ssh-rdp-stack",
            description: "Scans all security groups in the stack for SSH/RDP access from the internet.",
            enforcementLevel: "mandatory",
            validateStack: (args, reportViolation) => {
                const securityGroups = args.resources.filter(
                    (r) => r.type === "aws:ec2/securityGroup:SecurityGroup"
                );

                for (const sg of securityGroups) {
                    const ingress = sg.props.ingress || [];

                    for (const rule of ingress) {
                        const cidrBlocks = rule.cidrBlocks || [];
                        const fromPort = rule.fromPort;
                        const toPort = rule.toPort;

                        // Check if rule allows access from 0.0.0.0/0
                        const allowsPublicAccess = cidrBlocks.some(
                            (cidr: string) => cidr === "0.0.0.0/0"
                        );

                        if (allowsPublicAccess) {
                            // Check if SSH (22) or RDP (3389) ports are exposed
                            const exposesSSH = fromPort !== undefined && toPort !== undefined &&
                                fromPort <= 22 && toPort >= 22;
                            const exposesRDP = fromPort !== undefined && toPort !== undefined &&
                                fromPort <= 3389 && toPort >= 3389;

                            if (exposesSSH) {
                                reportViolation(
                                    `Security group '${sg.name}' (${sg.urn}) allows SSH (port 22) access from the internet (0.0.0.0/0). ` +
                                    `This is a security risk. Restrict access to specific IP addresses or remove this rule.`
                                );
                            }

                            if (exposesRDP) {
                                reportViolation(
                                    `Security group '${sg.name}' (${sg.urn}) allows RDP (port 3389) access from the internet (0.0.0.0/0). ` +
                                    `This is a security risk. Restrict access to specific IP addresses or remove this rule.`
                                );
                            }
                        }
                    }
                }
            },
        },
    ],
});
