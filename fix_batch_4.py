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

fixes = {
    262: [ # Ansible Idempotency
        "Ansible modules check the current state and only apply changes if the state differs from the desired configuration.",
        "The playbook executes every task regardless of the system state, but suppresses error messages for cleaner logs.",
        "A feature that automatically rolls back the entire deployment if a single task fails to complete successfully.",
        "The ability to run multiple playbooks in parallel across thousands of servers without causing network congestion."
    ],
    364: [ # Immutable Infrastructure Containers
        "Containers should never be patched or updated in place; replace them with a new image version instead.",
        "Containers should be logged into via SSH daily to apply the latest security patches and updates manually.",
        "Containers must use a persistent file system to ensure that all changes are saved across reboots.",
        "Containers should run a background process that automatically updates the application code from Git."
    ],
    365: [ # Docker Content Trust
        "A security feature that uses digital signatures to verify the integrity and publisher of Docker images.",
        "A paid subscription service that provides access to premium Docker images verified by Docker Inc.",
        "A firewall rule that prevents Docker containers from accessing the internet unless explicitly allowed.",
        "A peer-to-peer network for sharing Docker images between trusted developers in the same organization."
    ],
    425: [ # Least Privilege
        "Granting users and services only the minimum permissions necessary to perform their required tasks.",
        "Allowing all developers full admin access to production servers to ensure they can fix issues quickly.",
        "Creating a single shared root account for the entire team to simplify password management.",
        "Disabling all password requirements and relying solely on IP whitelisting for authentication."
    ],
    431: [ # DevOps Collaboration
        "Breaking down silos between teams, leading to faster problem solving and innovation.",
        "Combining all development and operations roles into a single person to save money.",
        "Holding daily meetings where every team member must report their status for at least 10 minutes.",
        "Forcing developers to write their own operations manuals before writing any code."
    ],
    230: [ # Virtualization
        "Creating virtual instances of computing resources (like VMs) on a single physical machine.",
        "Simulating a network connection between two computers that are not physically connected.",
        "Encrypting hard drives to prevent data theft in case of physical server theft.",
        "Running software in a special mode that uses 100% of the CPU for maximum performance."
    ],
    315: [ # Version Control
        "A system that records changes to a file or set of files over time so that you can recall specific versions later.",
        "A strict backup policy where every file is copied to an external hard drive every night at midnight.",
        "A software license management tool that prevents unauthorized users from running the application.",
        "A database feature that tracks which user logged in and what queries they executed for auditing."
    ],
    318: [ # Shift Left Security
        "Integrating security practices early in the development lifecycle (design/code) rather than waiting for the end.",
        "Moving the security team to the left side of the office building to sit closer to the developers.",
        "Focusing exclusively on securing the left-most bits of the encryption key to save processing power.",
        "Conducting security audits only after the product has been released to the public market."
    ],
    127: [ # Firewall Purpose
        "To monitor and control incoming and outgoing network traffic based on predetermined security rules.",
        "To speed up internet connection by compressing all data packets before they leave the network.",
        "To prevent physical fires in the data center by monitoring server temperature sensors.",
        "To automatically scan all email attachments for viruses before they reach the user's inbox."
    ],
    176: [ # WAF Function
        "To protect web applications by filtering and monitoring HTTP traffic between a web application and the Internet.",
        "To encrypt the database connection to prevent SQL injection attacks from internal users.",
        "To load balance traffic across multiple servers to ensure high availability during traffic spikes.",
        "To backup website files to a remote server automatically every time a change is detected."
    ],
    383: [ # Parallel Execution
        "Running independent jobs (like unit tests and linting) simultaneously to reduce total pipeline duration.",
        "Executing the same job multiple times on the same server to verify consistency of results.",
        "Running jobs on a supercomputer that uses parallel processing for faster mathematical calculations.",
        "Scheduling jobs to run one after another in a specific order to avoid resource contention."
    ],
    150: [ # Spot Instance
        "Unused EC2 capacity available at a significant discount, but can be interrupted with little notice.",
        "A dedicated server that is reserved for your exclusive use for a period of one or three years.",
        "A virtual machine that is optimized for high-performance graphics rendering and machine learning.",
        "A special instance type that is guaranteed to never be rebooted or terminated by the cloud provider."
    ],
    283: [ # Prometheus Exporters
        "Agents that collect and expose metrics from systems that don't output Prometheus metrics natively.",
        "Tools that export Prometheus data to a CSV file for analysis in Microsoft Excel.",
        "Plugins that forward logs from Prometheus to a centralized logging system like ELK.",
        "Scripts that automatically delete old metrics to free up disk space on the Prometheus server."
    ],
    326: [ # Orchestration
        "Automated configuration, coordination, and management of computer systems and software.",
        "The manual process of racking and stacking servers in a data center cabling layout.",
        "A musical arrangement performed by a group of developers typing in rhythm.",
        "The legal framework governing the relationships between cloud providers and customers."
    ],
    332: [ # GitOps
        "Using Git repositories as the source of truth for defining infrastructure and application state.",
        "Using Git to manage project management tasks like assigning tickets and tracking bugs.",
        "A command-line tool for visualizing the Git commit history as a tree graph.",
        "A backup strategy where the entire database is committed to a Git repository every hour."
    ],
    274: [ # ELB Function
        "Distributes incoming application traffic across multiple targets, such as EC2 instances.",
        "Encrypts data at rest on the connected EC2 instances for enhanced security.",
        "Automatically scales the number of EC2 instances based on CPU utilization metrics.",
        "Blocks malicious traffic from entering the network based on a set of firewall rules."
    ],
    356: [ # HPA vs VPA
        "HPA scales the number of pods (horizontal); VPA adjusts CPU/Memory requests of existing pods (vertical).",
        "HPA enables high performance availability; VPA enables virtual private access.",
        "HPA is used for stateful applications; VPA is used for stateless microservices.",
        "HPA scales the underlying nodes; VPA scales the containers within the nodes."
    ],
    275: [ # Object Storage
        "Storage architecture that manages data as objects, suitable for unstructured data like media.",
        "A relational database system optimized for storing JSON documents and XML files.",
        "A block storage device that appears to the operating system as a locally attached hard drive.",
        "A memory caching layer that improves the performance of read-heavy database queries."
    ],
    188: [ # K8s Network Policy
        "It defines how groups of Pods are allowed to communicate with each other and other network endpoints.",
        "It sets the bandwidth limits for the cluster to prevent any single pod from using too much data.",
        "It assigns a static IP address to every pod in the cluster to make them reachable from outside.",
        "It encrypts all traffic between nodes using a VPN tunnel for secure communication."
    ],
    195: [ # Bash Variables
        "Variables are defined without a dollar sign (e.g., `name=\"value\"`) and accessed with one (e.g., `$name`).",
        "Variables are declared using the `var` keyword and must be typed (e.g., `int count = 0`).",
        "Variables allow spaces around the equals sign (e.g., `name = value`) for better readability.",
        "Variables are global by default and cannot be scoped to a specific function or block."
    ],
    319: [ # Microservices Arch
        "Structuring an application as a collection of loosely coupled, independently deployable services.",
        "Writing all application code in a single file to minimize the overhead of file I/O operations.",
        "Using a single large database for all application data to ensure strict data consistency.",
        "Deploying the entire application as a monolithic binary on a massive mainframe server."
    ],
    331: [ # Feature Flag
        "A technique that allows you to turn features on or off without deploying new code.",
        "A comment in the code that marks a section as a new feature for documentation purposes.",
        "A GitHub label applied to pull requests that introduce new functionality to the codebase.",
        "A compiler flag that optimizes the binary for specific hardware features like AVX instructions."
    ],
    263: [ # Cloud Computing
        "The on-demand delivery of computing services over the internet with pay-as-you-go pricing.",
        "Running all applications on a local server that is connected to the internet via satellite.",
        "A grid computing network where idle home computers are used to process scientific data.",
        "Storing data on a USB drive that is carried around by the user for portability."
    ],
    185: [ # MAC Address
        "A unique hardware identifier assigned to network interfaces for communication at the Data Link Layer.",
        "A temporary address assigned by the router when a device connects to the Wi-Fi network.",
        "An encrypted key used to authenticate the device to the secure corporate network.",
        "A software-defined address that can be changed by the user to hide their identity."
    ],
    231: [ # Multi-Cloud Strategy
        "Using services from multiple cloud providers (e.g., AWS + Azure) to avoid vendor lock-in.",
        "Backing up data to multiple hard drives in different physical locations for redundancy.",
        "Running the same application on multiple servers within the same data center.",
        "Using multiple accounts with the same cloud provider to separate billing for departments."
    ],
    268: [ # Virtualization (Dup of 230? Different ID)
        "Creating virtual instances of servers, storage, or networks on a single physical server.",
        "Using a VR headset to inspect the 3D model of the data center infrastructure.",
        "Running a simulation of the network traffic to predict bottlenecks before they happen.",
        "Storing files in the cloud so they can be accessed from any device with an internet connection."
    ],
    285: [ # Grafana Usage
        "Visualizing time-series data from sources like Prometheus via interactive dashboards.",
        "Storing long-term historical log data for compliance and auditing purposes.",
        "Sending email alerts to the on-call engineer when a server goes down.",
        "Managing user authentication and authorization for the entire DevOps platform."
    ],
    329: [ # Canary Release
        "Rolling out a new feature to a small subset of users to test it before a full rollout.",
        "Deploying code to a server named 'Canary' that is used for internal testing only.",
        "Releasing a version of the software that automatically reports bugs to the developer.",
        "A deployment strategy that uses yellow-colored loading bars to indicate progress."
    ],
    330: [ # Dark Launching
        "Releasing code to production that is turned off by a feature toggle, invisible to users.",
        "Deploying code during the night when user traffic is at its lowest point.",
        "Releasing a version of the app with a dark mode theme enabled by default.",
        "Launching a product without any marketing or announcement to test organic growth."
    ],
    343: [ # Infrastructure Drift
        "When the actual state of infrastructure deviates from the configuration defined in IaC code.",
        "The physical movement of servers within a data center due to floor vibrations.",
        "The gradual degradation of hardware performance over time due to component aging.",
        "Moving infrastructure from one cloud provider to another to save costs."
    ],
    411: [ # Chaos Monkey (Dup of 5? but ID 411)
        "A tool invented by Netflic that randomly terminates instances in production to ensure that engineers implement their services to be resilient to instance failures.",
        "A script that randomly renames files in the database to test the system's error handling.",
        "A security scanner that attempts to brute-force passwords to check for weak credentials.",
        "A load balancer that randomly drops packets to simulate a poor network connection."
    ],
    125: [ # Hybrid Cloud (Dup?)
        "A computing environment that combines a public cloud and a private cloud/on-premises infrastructure.",
        "A cloud provider that offers both Windows and Linux virtual machines.",
        "A storage system that uses both SSDs and HDDs for optimal performance.",
        "A network that uses both fiber optic and copper cables for redundancy."
    ],
    156: [ # Subnet Mask Function
        "It determines which part of the IP address is the network portion and which is the host portion.",
        "It encrypts the IP address to hide the user's location from websites.",
        "It speeds up the network connection by masking the latency of long-distance routes.",
        "It blocks access to specific websites based on a blacklist of known malicious IPs."
    ],
    181: [ # SSO Advantage
        "It improves user experience and productivity by requiring only one set of credentials for multiple apps.",
        "It forces users to change their password every week to improve security.",
        "It allows users to log in without a password by using a physical hardware key.",
        "It encrypts the user's session data to prevent session hijacking attacks."
    ],
    229: [ # Serverless (Dup?)
        "Developers run code without provisioning or managing servers; resources are allocated dynamically.",
        "Running applications on a dedicated server that is managed by a third-party MSP.",
        "Using peer-to-peer networking to distribute the workload across client devices.",
        "A marketing term for using bare-metal servers instead of virtual machines."
    ],
    320: [ # Monolith
        "An application built as a single, unified unit where all logic is tightly coupled.",
        "A large stone monument placed in the lobby of the tech company's headquarters.",
        "A single server that hosts all the applications for the entire organization.",
        "A database that has grown so large it can no longer be backed up successfully."
    ],
    357: [ # PVC
        "A request for storage by a user, which consumes persistent volume (PV) resources.",
        "A plastic material used to insulate network cables in the data center.",
        "A backup file that contains the entire contents of a persistent volume.",
        "A permission setting that allows a container to write to the host filesystem."
    ],
    439: [ # Cross-Functional Team
        "A group of people with different functional expertise working toward a common goal.",
        "A team that works across multiple time zones to ensure 24/7 coverage.",
        "A group of developers who are proficient in multiple programming languages.",
        "A management team that oversees multiple different projects simultaneously."
    ],
    251: [ # Latency
        "The delay before a transfer of data begins following an instruction for its transfer.",
        "The speed at which data travels through the fiber optic cables.",
        "The amount of data that can be transmitted in a given amount of time.",
        "The percentage of data packets that are lost during transmission."
    ],
    324: [ # Config Mgmt
        "The process of maintaining systems, servers, and software in a desired, consistent state.",
        "Manually editing configuration files on each server to ensure they are correct.",
        "A database that stores all the user preferences and settings for the application.",
        "The job of the project manager to configure the Jira board for the team."
    ],
    211: [ # set -e
        "It aborts the script execution immediately if any command returns a non-zero exit code.",
        "It enables the script to run in the background as a daemon process.",
        "It encrypts the script output to prevent sensitive data from leaking into logs.",
        "It sets the environment variables for the script from a local .env file."
    ],
    239: [ # CDN
        "A distributed network of servers that caches content close to users for faster delivery.",
        "A centralized database that stores all the multimedia content for the website.",
        "A private network used by content creators to upload large video files.",
        "A security system that scans user-uploaded content for copyright infringement."
    ],
    278: [ # IAM Role
        "Grants permissions to entities (like EC2 instances) without long-term credentials.",
        "A user account that has read-only access to the AWS billing dashboard.",
        "A policy that enforces multi-factor authentication for all root users.",
        "A group of users who are allowed to access the production database."
    ],
    346: [ # Policy as Code
        "Defining and enforcing security and compliance rules using code (e.g., Open Policy Agent).",
        "Writing the employee handbook in Markdown and storing it in a Git repository.",
        "Using a specialized programming language to draft legal contracts for vendors.",
        "Hardcoding the password policy into the login form's JavaScript validation."
    ],
    233: [ # AZ
        "A physically separate data center within a cloud region, designed for fault tolerance.",
        "A reserved area of the hard drive that is used for backing up critical system files.",
        "A network segment that is isolated from the internet for hosting sensitive data.",
        "A time zone that is used for scheduling maintenance windows to minimize impact."
    ],
    260: [ # Inline script (Dup?)
        "Running a script directly inside a pipeline configuration (e.g., GitHub Actions run command).",
        "A script that is embedded in the HTML code of a web page to handle events.",
        "A SQL script that is executed as part of a database migration transaction.",
        "A Python script that is imported into another script as a module."
    ],
    193: [ # Bash Feature
        "It is interpreted by the shell and used for automating command-line tasks in Unix-like systems.",
        "It is a compiled language that produces binary executables for high performance.",
        "It is strictly object-oriented and requires defining classes for every script.",
        "It is only available on Linux and cannot be used on macOS or Windows systems."
    ]
}

def apply_batch4():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        count = 0
        for q_id, distractors in fixes.items():
            # fetch correct answer
            cur.execute("SELECT correct_answer FROM quiz_questions WHERE id = %s", (q_id,))
            res = cur.fetchone()
            if not res:
                continue
            correct_ans = res[0]
            
            # ensure 0 is correct
            distractors[0] = correct_ans
            
            # update
            cur.execute("UPDATE quiz_questions SET options = %s WHERE id = %s", (json.dumps(distractors), q_id))
            count += 1
            
        conn.commit()
        print(f"Batch 4 updated {count} questions.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    apply_batch4()
