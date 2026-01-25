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

# Dictionary of ID -> New Options List
# The correct answer MUST be included in the list.

new_fixes = {
    402: [ # GitOps
        "Operational framework that takes DevOps best practices used for application development (version control, collaboration, compliance) and applies them to infrastructure automation.", # Correct
        "A proprietary Git workflow that mandates forcing all commits to the main branch immediately to ensure rapid deployment velocity without peer review.",
        "A plugin for Jenkins that automatically synchronizes the local file system with a remote Git repository every five minutes to prevent data loss.",
        "A database management strategy that uses Git commit hashes as primary keys to ensure data integrity across distributed clusters."
    ],
    408: [ # SLA - I might have fixed it in prev batch by text matching, but ID match is safer.
        "A commitment between a service provider and a client. Particular aspects of the service – quality, availability, responsibilities – are agreed between the service provider and the service user.", # Correct
        "A strictly internal document used by developers to track the estimated time required to complete a specific feature request or bug fix.",
        "A marketing brochure that outlines the theoretical maximum performance capabilities of the system under ideal laboratory conditions.", 
        "A legal disclaimer that absolves the service provider of all responsibility in the event of a catastrophic data center failure."
    ],
    360: [ # CrashLoopBackOff
        "Ideally, a Pod is crashing repeatedly, and Kubernetes is backing off (waiting longer) before trying to restart it again.", # Correct
        "The network loopback interface has crashed and the kernel is attempting to restore connectivity to the local host.",
        "A circular dependency has been detected in the deployment configuration, preventing the application from starting up.",
        "The container has successfully completed its task and is now waiting for a manual trigger to restart the process."
    ],
    313: [ # Silo
        "An isolated team or department that does not share information or processes with others, hindering collaboration.", # Correct
        "A specialized server rack designed to isolate high-performance computing nodes from the rest of the network.",
        "A secure storage container used for archiving long-term backup tapes in a climate-controlled environment.",
        "A software architecture pattern where all data is stored in a single monolithic database table."
    ],
    400: [ # Immutable Infrastructure
        "Infrastructure that is never modified after deployment; if changes are needed, new infrastructure is built to replace the old.", # Correct
        "Servers that are locked down so tightly that even system administrators cannot log in to perform maintenance tasks.",
        "A legacy infrastructure setup that is too expensive and risky to migrate to modern cloud platforms.",
        "A data persistence layer that guarantees records can never be deleted or updated once written."
    ],
    406: [ # 12-Factor App Usage
        "Ideally suited for developing software-as-a-service apps, focusing on portability and automated deployment.", # Correct
        "Specifically designed for monolithic desktop applications that require direct hardware access key.",
        "A framework intended primarily for embedded systems with limited processing power and memory.", 
        "A methodology for managing physical supply chains in manufacturing industries efficiently."
    ],
    221: [ # Inline Script
        "A script written directly inside the pipeline configuration file (e.g., within `run:` key) rather than in a separate file.", # Correct
        "A script that is executed in the background while the main application continues to run asynchronously.",
        "A client-side JavaScript file that is injected into the HTML page to track user interactions.",
        "A database migration script that runs automatically whenever the schema version changes."
    ],
    354: [ # Labels and Selectors
        "Labels are key/value pairs attached to objects; Selectors allow you to filter/select objects based on their labels.", # Correct
        "Labels are unique identifiers for pods; Selectors are used to assign static IP addresses to them.",
        "Labels define the resource limits for a container; Selectors choose which node the pod should run on.",
        "Labels are security tags for access control; Selectors encrypt traffic between labeled pods."
    ],
    388: [ # Policy-as-Code
        "Writing code to define and enforce policies (security, compliance) rather than configuring them manually in a GUI.", # Correct
        "Using a proprietary programming language to write legal contracts for service level agreements.",
        "Hardcoding security rules directly into the application source code to prevent tampering.",
        "Generating human-readable PDF policy documents automatically from the Git commit history."
    ],
    410: [ # SLI
        "A quantitative measure of some aspect of the level of service that is provided (e.g., latency, error rate).", # Correct
        "A qualitative assessment of user satisfaction derived from customer support ticket sentiment analysis.", 
        "A high-level business goal that defines the target revenue growth for the upcoming quarter.",
        "A list of all the software libraries and dependencies used in the application build process."
    ],
    395: [ # Pod Security Policies
        "To control security sensitive aspects of the pod specification, such as preventing privileged containers.", # Correct
        "To encrypt all network traffic entering and leaving the pod using mutual TLS authentication.",
        "To automatically scan container images for known vulnerabilities before they are pulled.",
        "To restrict the CPU and memory usage of a pod to prevent it from starving other workloads."
    ],
    371: [ # Pipeline Trigger
        "An event that automatically starts a pipeline execution (e.g., code push, pull request, scheduled time).", # Correct
        "A manual button that must be pressed by a manager to approve a deployment to production.",
        "A failed test case that causes the entire build process to stop immediately and report an error.",
        "A notification sent to the development team whenever a new bug is reported by a user."
    ],
    191: [ # Goal of Automation
        "To eliminate manual effort in repetitive tasks like deployment and provisioning to increase efficiency and reliability.", # Correct
        "To replace all human engineers with artificial intelligence agents that write code autonomously.",
        "To increase the complexity of the system so that it requires specialized knowledge to operate.",
        "To reduce the frequency of deployments to ensure that the system remains stable for longer periods."
    ],
    303: [ # Elasticsearch Optimization
        "Use 'filter' context (cached) instead of 'query' context where possible, and avoid leading wildcard searches.", # Correct
        "Increase the number of replica shards to match the number of worker nodes in the cluster exactly.",
        "Disable all data indexing to maximize write throughput at the cost of search capability.",
        "Run all queries with the highest possible priority flag to override system resource limits."
    ],
    376: [ # TDD
        "It ensures high test coverage and reliable automated tests, which are the gatekeepers of any CI/CD pipeline.", # Correct
        "It slows down development significantly by forcing developers to write tests before understanding the requirements.",
        "It replaces manual QA teams entirely, allowing developers to push code directly to production without checks.",
        "It focuses solely on unit testing and ignores integration or end-to-end testing scenarios."
    ],
    382: [ # SAST vs DAST
        "Static (SAST) creates scans of source code at rest; Dynamic (DAST) scans the running application for vulnerabilities.", # Correct
        "SAST is performed manually by security experts; DAST is fully automated by AI bots.",
        "SAST checks for performance bottlenecks; DAST checks for security loopholes and bugs.",
        "SAST is used for frontend code; DAST is used exclusively for backend database queries."
    ],
    246: [ # Kubernetes
        "An open-source system for automating deployment, scaling, and management of containerized applications.", # Correct
        "A proprietary cloud platform provided by Google for hosting virtual machines and storage buckets.",
        "A lightweight container runtime that replaces Docker for local development environments.",
        "A configuration management tool used to provision physical servers in a data center."
    ],
    129: [ # Agile
        "An iterative approach to project management and software development that helps teams deliver value to their customers faster.", # Correct
        "A rigid project management framework that requires detailed planning and documentation before any coding begins.",
        "A software development methodology that prioritizes tools and processes over individuals and interactions.",
        "A technique for writing code quickly without regard for long-term maintainability or testing."
    ],
    328: [ # Blue-Green
        "A technique that reduces downtime and risk by running two identical production environments called Blue and Green.", # Correct
        "A deployment strategy where new features are released to a small subset of users (Green) before everyone else (Blue).",
        "A method of color-coding server racks in the data center to distinguish between production and staging.",
        "A security protocol that flags trusted traffic as Green and suspicious traffic as Blue for analysis."
    ],
    426: [ # Secret Rotation
        "The practice of regularly changing secrets (passwords, keys) to minimize the risk of them being compromised.", # Correct
        "The automated process of moving secrets between different storage vaults to confuse potential attackers.",
        "A cryptographic technique that shifts the bits of a key cyclically to generate new session tokens.",
        "Hiding secrets in different parts of the source code to make them harder to find."
    ],
    300: [ # Hot-Warm-Cold
        "A data tiering strategy to optimize cost and performance: Hot (frequent I/O), Warm (read-only), Cold (archival).", # Correct
        "A server cooling mechanism that adjusts fan speeds based on the CPU temperature zones.",
        "A backup schedule where Hot is hourly, Warm is daily, and Cold is weekly backups.",
        "A deployment pipeline with three stages: Hot (Dev), Warm (Staging), and Cold (Production)."
    ],
    351: [ # K8s HA
        "By using multiple master nodes (control plane) and replicating application pods across multiple worker nodes.", # Correct
        "By relying on a single powerful supercomputer that can handle all failures without downtime.",
        "By automatically restarting the entire cluster every night to clear out memory leaks.",
        "By storing all data in a single shared database that is backed up to tape drives daily."
    ],
    361: [ # Cgroups
        "To limit, account for, and isolate the resource usage (CPU, memory, I/O) of a collection of processes.", # Correct
        "To group containers together logically so they can be managed as a single application unit.", 
        "To define access control lists for users belonging to different departments or teams.", 
        "To organize source code files into logical folders within a large monorepo structure."
    ],
    401: [ # Rolling Deployment
        "Replacing instances of the old version with the new version one by one (or in batches) to ensure zero downtime.", # Correct
        "Deploying the new version to a separate environment and switching traffic instantly via DNS.",
        "Stopping all servers simultaneously, updating the code, and then restarting them all at once.",
        "Releasing the new version only to internal employees before rolling it out to public users."
    ],
    416: [ # Multi-Cloud Mgmt
        "By using cloud-agnostic tools like Terraform and Kubernetes that abstract away the underlying provider differences.", # Correct
        "By manually logging into each cloud provider's console and configuring resources individually.",
        "By using a single cloud provider exclusively to avoid the complexity of managing multiple platforms.",
        "By hiring separate teams for each cloud provider and keeping them completely isolated from each other."
    ],
    344: [ # FinOps
        "Financial Operations - practicing cloud financial management to optimize spend and get maximum value.", # Correct
        "Financial Options - a trading strategy used by tech companies to hedge against currency fluctuations.", 
        "Finished Operations - the state of a project after it has been successfully deployed to production.", 
        "Fine-grained Operations - a micro-management style that focuses on small details of daily work."
    ],
    223: [ # Ansible Idempotency
        "Modules check the current state of the system and only apply changes if the state does not match the desired configuration.", # Correct
        "The script runs repeatedly in a loop until it receives a success signal from the target server.", 
        "The system creates a backup of the configuration before applying any changes to allow for easy rollback.", 
        "Every task generates a unique ID that prevents it from being executed more than once per day."
    ],
    296: [ # Grafana Annotations
        "To mark specific events (like deployments or outages) on graphs to correlate them with metric changes.", # Correct
        "To add comments to the dashboard code to explain complex queries to other developers.", 
        "To label specific users who have access to view sensitive data on the dashboard.", 
        "To highlight metrics that have exceeded their defined threshold limits in red."
    ],
    432: [ # Runbook
        "A compilation of routine procedures and operations that the system administrator or operator carries out.", # Correct
        "A log file that records the runtime duration of every job executed by the CI server.", 
        "A script that automatically runs whenever the server boots up to initialize services.", 
        "A physical book kept in the server room containing emergency contact numbers."
    ],
    441: [ # Scrum
        "An agile framework for managing knowledge work, with an emphasis on software development.", # Correct
        "A disorganized method of working where team members scramble to fix bugs at the last minute.", 
        "A rugby term used to describe the chaotic environment of a startup company.", 
        "A strict waterfall process where every phase must be completed before the next begins."
    ],
    224: [ # Cloud Computing
        "The on-demand delivery of computing services (servers, storage, etc.) over the internet with pay-as-you-go pricing.", # Correct
        "A network of satellites providing internet connectivity to remote areas without ground infrastructure.", 
        "Using weather patterns to predict server load and optimize cooling efficiency in data centers.", 
        "Storing data exclusively on local hard drives to prevent unauthorized access from the internet."
    ],
   132: [ # Object Storage
        "A storage architecture that manages data as objects (data + metadata + ID), scalable and accessible via API.", # Correct
        "A database that stores data in rows and columns, optimized for complex transactional queries.", 
        "A file system hierarchy that organizes files into folders and subdirectories on a disk.", 
        "A type of RAM module that stores temporary object data for faster processing speed."
    ],
    141: [ # Continuous Deployment
        "Every change that passes all stages of your production pipeline is released to your customers automatically.", # Correct
        "Developers manually deploy their changes to production whenever they feel the code is ready.", 
        "Changes are deployed to a staging environment daily, but production releases happen only once a month.", 
        "The system continuously monitors the production server and restarts it if it crashes."
    ],
    154: [ # IPv4 vs IPv6
        "IPv4 uses 32-bit addresses (approx 4.3 billion), while IPv6 uses 128-bit addresses (virtually infinite).", # Correct
        "IPv4 is faster and more secure than IPv6, which is why it is still the dominant standard.", 
        "IPv4 uses hexadecimal notation, while IPv6 uses decimal notation for easier readability.", 
        "IPv4 is designed for private networks, while IPv6 is used exclusively for the public internet."
   ],
   355: [ # Ingress
        "An API object that manages external access to services in a cluster, typically HTTP/HTTPS.", # Correct
        "A firewall rule that blocks all incoming traffic to the cluster except for SSH connections.", 
        "A storage volume that allows data to be imported into the cluster from external sources.", 
        "A log aggregator that collects incoming log streams from all pods in the namespace."
   ],
   161: [ # SSH vs Telnet
        "SSH encrypts all communication, while Telnet sends data (including passwords) in plain text.", # Correct
        "SSH is a legacy protocol that has been replaced by the faster and more modern Telnet.", 
        "SSH only works on Linux systems, while Telnet is compatible with all operating systems.", 
        "SSH requires a paid license, while Telnet is free and open-source software."
   ],
   267: [ # Serverless
        "Running applications without managing the underlying infrastructure; resources are allocated dynamically.", # Correct
        "Hosting applications on a physical server that does not have an operating system installed.", 
        "Running code on a decentralised blockchain network where no single server exists.", 
        "Using a server that is completely disconnected from the internet for maximum security."
   ]
}

def apply_batch_fixes():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        count = 0
        for q_id, distractors in new_fixes.items():
            # Get correct answer to ensure consistency/safety
            cur.execute("SELECT correct_answer FROM quiz_questions WHERE id = %s", (q_id,))
            res = cur.fetchone()
            if not res:
                print(f"Skipping ID {q_id}, not found.")
                continue
            
            correct_ans = res[0]
            
            # Use manual list but verify correct answer is 0th index
            # (My list assumes 0th index IS correct answer manually copied)
            # Re-ensure it.
            if distractors[0] != correct_ans:
                 print(f"Warning: Manual correct answer for ID {q_id} might differ from DB. Using DB's correct answer + Manual distractors.")
                 # distractors[0] is my manual correct answer. If it differs slightly from DB, I should maybe use the DB one to be safe, 
                 # or update DB correct answer too? 
                 # Safer: Replace distractors[0] with DB correct answer to avoid breaking string equality logic in checking.
                 distractors[0] = correct_ans
            
            # Update DB
            cur.execute("UPDATE quiz_questions SET options = %s WHERE id = %s", (json.dumps(distractors), q_id))
            count += 1
            
        conn.commit()
        print(f"Batch updated {count} questions.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    apply_batch_fixes()
