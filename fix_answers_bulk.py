import psycopg2
import json
import os

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        database=os.environ.get('DB_NAME', 'quiz_project'),
        user=os.environ.get('DB_USER', 'admin'),
        password=os.environ.get('DB_PASSWORD', 'password123')
    )

bulk_updates = {
    4: [ # SRE Goal
        "Applying software engineering principles to operations to improve system reliability.",
        "Maximizing feature velocity by reducing testing time and bypassing standard controls.",
        "Migrating all on-premise infrastructure to serverless cloud architectures exclusively.",
        "Isolating development teams from operations to ensure specialized focus."
    ],
    5: [ # SIEM
        "Aggregating and analyzing security data from multiple sources.",
        "Encrypting data at rest across all enterprise storage systems.",
        "Managing identity verification and access control policies.",
        "Filtering incoming network traffic based on firewall rules."
    ],
    6: [ # Subnet Mask
        "It divides an IP address into network and host portions.",
        "It translates private IP addresses to public IPs for routing.",
        "It encrypts payload data within IP packets for security.",
        "It determines the physical path packets take through routers."
    ],
    9: [ # CI
        "Frequent integration of code into a shared repository with automated testing.",
        "Continuous deployment of code changes to production environments automatically.",
        "Integrating security scanning into the later stages of the development lifecycle.",
        "Automating infrastructure provisioning using configuration management tools."
    ],
    10: [ # Terraform Module
        "To organize and reuse Terraform configurations.",
        "To manage remote state locking and consistency.",
        "To defined secure secrets for sensitive data.",
        "To enable multi-cloud resource provisioning."
    ],
    11: [ # DNS
        "It translates domain names into IP addresses.",
        "It routes data packets between different networks.",
        "It assigns IP addresses dynamically to devices.",
        "It establishes secure encrypted connections."
    ],
    18: [ # Ansible Inventory
        "A list of managed servers and their connection details.",
        "A collection of playbooks defining system configurations.",
        "A registry of available modules and their documentation.",
        "A secure vault for storing sensitive credentials."
    ],
    19: [ # Ephemeral Ports
        "Temporary ports used by client applications for outbound connections.",
        "Reserved ports assigned to specific standard network services.",
        "Blocked ports that configured to reject all incoming traffic.",
        "Virtual ports used for internal container communication."
    ],
    20: [ # K8s Secrets
        "Encrypting them at rest and using external vaults.",
        "Encoding them in Base64 and storing in Git repos.",
        "Injecting them as environment variables in Pods.",
        "Storing them in ConfigMaps with restricted access."
    ],
    21: [ # PowerShell vs Bash
        "It is object-oriented, passing objects instead of text streams.",
        "It uses a strictly imperative syntax unlike Bash's declarative style.",
        "It is designed primarily for text processing and manipulation.",
        "It runs exclusively on the Windows operating system kernel."
    ],
    22: [ # Region vs AZ
        "A Region is a geographic area, while an AZ is an isolated data center within that region.",
        "A Region is a logical grouping of users, whilst an AZ is a physical server location.",
        "A Region provides global content delivery, while an AZ handles local compute.",
        "A Region defines tax jurisdiction, while an AZ defines data sovereignty."
    ],
    23: [ # set -e
        "It causes the script to exit immediately if any command returns a non-zero status.",
        "It enables verbose logging mode to print each command before execution.",
        "It forces the script to execute remaining commands even after a failure.",
        "It exports all defined variables to the environment of child processes."
    ],
    27: [ # Docker Multi-stage
        "To create smaller, more secure final images by copying artifacts from build stages.",
        "To build images for multiple processor architectures simultaneously in parallel.",
        "To allowing running multiple services within a single container instance.",
        "To speed up build times by caching intermediate layers on remote servers."
    ],
    28: [ # Jenkins Shared Lib
        "A reusable collection of Groovy scripts that can be used across multiple pipelines.",
        "A plugin repository for extending Jenkins functionality with community tools.",
        "A distributed storage system for managing build artifacts and dependencies.",
        "A set of pre-configured docker images for running build agents."
    ],
    29: [ # mTLS
        "A protocol where both the client and server authenticate each other using certificates.",
        "A method for encrypting traffic between a load balancer and backend servers.",
        "A standard for securing email communications using asymmetric encryption.",
        "A VPN protocol for tunneling insecure traffic over a public network."
    ],
    31: [ # DaemonSet
        "A controller that ensures a copy of a Pod runs on selected nodes (usually all nodes).",
        "A deployment strategy that rolls out updates to a specific subset of users.",
        "A service type that balances traffic across a set of stateful pods.",
        "A job that runs to completion on a specific schedule or trigger."
    ],
    37: [ # /proc
        "A virtual filesystem exposing kernel and process information.",
        "A system directory containing device driver configuration files.",
        "A temporary runtime directory for storing variable data files.",
        "A protected directory for storing kernel modules and binaries."
    ],
    54: [ # Auto Scaling
        "Automatically adjusting the number of computing resources based on load.",
        "Automatically distributing network traffic across multiple servers.",
        "Automatically recovering failed instances by restarting them.",
        "Automatically upgrading applications to the latest version."
    ],
    57: [ # XSS
        "A vulnerability where attackers inject malicious scripts into web pages viewed by other users.",
        "A technique for hijacking user sessions by stealing authentication tokens.",
        "A method of bypassing firewall restrictions using tunneling protocols.",
        "A database injection attack exposing sensitive user information."
    ],
    58: [ # 12-Factor App
        "A set of best practices for building modern, scalable, cloud-native applications.",
        "A methodology for agile project management in distributed teams.",
        "A security framework for compliance with data protection regulations.",
        "A standardized approach for designing RESTful API interfaces."
    ],
    59: [ # Lead Time for Changes
        "The time it takes for a code commit to be successfully deployed to production.",
        "The time required to resolve a production incident after detection.",
        "The average time a developer spends coding a new feature.",
        "The duration of the systematic code review process."
    ],
    71: [ # CloudFormation Condition
        "By defining a Condition in the template and referencing it in the resource's Condition field.",
        "By using intrinsic `Fn::If` functions within the resource properties block.",
        "By splitting the template into multiple stacks and deploying selectively.",
        "By using template parameters to dynamically enable or disable resources."
    ],
    73: [ # Intrinsic Functions
        "Built-in functions like `!Sub` or `!Ref` used to assign values dynamically at runtime.",
        "External Lambda functions invoked during stack creation for custom logic.",
        "Template macros that expand shorthand syntax into full resource definitions.",
        "Helper scripts used to validate template syntax before deployment."
    ],
    75: [ # Terraform Data Source
        "A configuration to fetch data from external/existing resources without managing them.",
        "A module used to initialize backend state storage configurations.",
        "A resource type that defines the schema for input variables.",
        "A provider plugin that enables interaction with specific APIs."
    ],
    77: [ # Terraform Circular Dependency
        "It builds a Directed Acyclic Graph (DAG) and errors out if a cycle is detected.",
        "It automatically resolves the cycle by provisioning resources in parallel.",
        "It prompts the user to manually define the dependency order.",
        "It ignores the dependency and attempts eventual consistency."
    ],
    79: [ # Sentinel
        "A policy-as-code framework to enforce compliance rules before provisioning infrastructure.",
        "A monitoring agent for tracking the health of Terraform runs.",
        "A secret management solution for securely improved credential storage.",
        "A service discovery tool for dynamic infrastructure environments."
    ],
    80: [ # Terraform Restore
        "Manually restore the previous `terraform.tfstate` file from version control or backup.",
        "Run the `terraform undo` command to revert the last applied changes.",
        "Use the `terraform refresh` command to rebuild the state from reality.",
        "Delete the state file and let Terraform regenerate it automatically."
    ],
    81: [ # terraform refresh
        "It updates the local state file to match the real-world infrastructure without modifying resources.",
        "It re-downloads all provider plugins and modules to the local cache.",
        "It destroys and recreates all resources to ensure a clean state.",
        "It validates the configuration syntax and checks for errors."
    ],
    96: [ # Elasticity
        "The ability to scale resources up or down dynamically based on demand.",
        "The ability to recover quickly from infrastructure failures.",
        "The ability to distribute traffic across multiple regions.",
        "The ability to support multiple operating systems seamlessly."
    ],
    101: [ # Git Commit Structure
        "It contains the tree ID, parent commit ID(s), author info, committer info, and the commit message.",
        "It contains the full snapshot of the project files at that point in time.",
        "It contains a diff of changes compared to the previous commit.",
        "It contains pointers to the modified files and their metadata."
    ],
    104: [ # Git GC
        "Optimizes repository by packing loose objects, removing unreachable objects, and updating references.",
        "Verifies the integrity of the commit history and repairs corrupted objects.",
        "Deletes old branches that have been merged into the main line.",
        "Archives the repository history to a separate backup file."
    ],
    107: [ # Reflog
        "A local log of all reference updates (HEAD movements) used to recover lost commits.",
        "A remote log of all push and pull events on the server.",
        "A history of all file changes indexed by commit hash.",
        "A cache of recently accessed objects for performance."
    ],
    110: [ # Git Conflict Markers
        "With special markers: <<<<<<<, =======, >>>>>>>",
        "By creating temporary .conflict files for manual resolution.",
        "By locking the file and preventing further edits.",
        "By reverting the file to the common ancestor version."
    ],
    112: [ # KISS
        "Comparing to complexity, simplicity should be a key goal in design, and unnecessary complexity should be avoided.",
        "Code should always be written in the fewest lines possible regardless of readability.",
        "Systems should only use proven legacy technologies to ensure stability.",
        "Development speed is the primary metric for project success."
    ],
     115: [ # White-box Monitoring
        "Monitoring based on metrics exposed by the internals of the system (e.g., logs, JVM stats).",
        "Monitoring user-facing endpoints to verify availability and latency.",
        "Monitoring performed by internal teams rather than external vendors.",
        "Monitoring that focuses on security compliance and audit logs."
    ],
    116: [ # Black-box Monitoring
        "Monitoring externally visible behavior as a user sees it (e.g., HTTP availability).",
        "Monitoring internal system states and performance counters.",
        "Monitoring performed by automated tools without human intervention.",
        "Monitoring that is completely opaque to the development team."
    ]
}

def update_bulk():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        count = 0
        for q_id, new_opts in bulk_updates.items():
            # Get correct answer to ensure consistency
            cur.execute("SELECT correct_answer FROM quiz_questions WHERE id = %s", (q_id,))
            res = cur.fetchone()
            if not res:
                continue
            
            correct_ans = res[0]
            
            # Ensure proper overwrite of the correct option
            # The first item in my manual list is always the correct one (copied from dump/logic).
            # But I will double check.
            new_opts[0] = correct_ans
            
            # Update DB
            cur.execute("UPDATE quiz_questions SET options = %s WHERE id = %s", (json.dumps(new_opts), q_id))
            count += 1
            
        conn.commit()
        print(f"Bulk updated {count} questions.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    update_bulk()
