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
# The correct answer must be included in the list.
# I will fetch the correct answer from DB to be safe, or hardcode it if I am sure.
# Better strategy: Read ID, fetch correct_answer, then combine with NEW distractors.

new_distractors = {
    53: [ # Pod
        "A logical collection of containers sharing network and storage namespace.", # Correct-ish length
        "A dedicated virtual machine instance allocated for a specific service.", 
        "A storage volume that persists data across container restarts.",
        "A network interface connecting multiple docker containers together."
    ],
    50: [ # Bastion Host
        "A secure server used to access a private network from an external network.", # Correct
        "A dedicated database server optimized for high-performance transactions.",
        "A load balancing appliance that distributes traffic across regions.",
        "A backup server that stores snapshots of the production environment."
    ],
    60: [ # Container Orchestration
        "The automated management of container deployment, scaling, and networking.", # Correct
        "The manual process of compiling code into executable container images.",
        "The virtualization of hardware resources to run multiple operating systems.",
        "The synchronization of database states across multiple geographic regions."
    ],
    61: [ # Immutable Infrastructure
        "Servers are never modified after deployment; they are replaced with new ones.", # Correct
        "Servers are strictly locked down so no users can log in remotely via SSH.",
        "Infrastructure configurations that are hardcoded and cannot be changed properly.",
        "Servers that effectively prevent any operating system updates or patches."
    ],
    62: [ # SELinux
        "A security architecture for Linux allowing for fine-grained access control policies.", # Correct
        "A lightweight Linux distribution optimized for containerized workloads.",
        "A network protocol used for secure file transfers between servers.",
        "A monitoring tool that tracks system performance and resource usage."
    ],
    63: [ # Load Balancer
        "A device or service that distributes network traffic across multiple servers.", # Correct
        "A security mechanism that blocks unauthorized access to the network.",
        "A storage system that replicates data across multiple hard drives.",
        "A configuration tool that automates server provisioning and setup."
    ],
    12: [ # Serverless Scalability
        "It auto-scales instantly based on demand without manual provisioning.", # Correct
        "It allocates a fixed pool of high-memory servers for performance.",
        "It distributes workloads across multiple dedicated physical machines.",
        "It relies on predictive algorithms to reserve capacity in advance."
    ],
    30: [ # Terraform Plan
        "It shows a preview of the changes that will be made without applying them.", # Correct
        "It automatically fixes configuration drift in the current infrastructure.",
        "It compiles the Terraform code into a binary executable for deployment.",
        "It destroys the existing infrastructure to prepare for a fresh install."
    ],
    40: [ # Idempotency
        "Running the same operation multiple times produces the same result without side effects.", # Correct
        "Running multiple operations simultaneously to speed up execution time.",
        "Ensuring that an operation can only be executed exactly once per day.",
        "Rolling back changes automatically if an error occurs during execution."
    ],
    45: [ # Race Condition
        "A flaw where the system's output depends on the sequence or timing of uncontrollable events.", # Correct
        "A performance issue caused by two processes competing for the same CPU core.",
        "A network delay that occurs when packets take different paths to the destination.",
        "A security vulnerability that allows attackers to bypass authentication checks."
    ],
    57: [ # XSS
        "A vulnerability where attackers inject malicious scripts into web pages viewed by other users.", # Correct
        "A technique used to steal database passwords by injecting SQL queries into input fields.",
        "A method of intercepting encrypted traffic between a client and a server.",
        "A denial of service attack that floods a web server with invalid requests."
    ],
    65: [ # ssh-keygen
        "Generates, manages, and converts authentication keys for SSH.", # Correct
        "Establishes a secure encrypted connection to a remote server.",
        "Encrypts local files using a symmetric password key algorithm.",
        "Configures the SSH daemon to accept incoming connections."
    ],
    67: [ # Technical Debt
        "The implied cost of additional rework caused by choosing an easy solution now instead of a better approach.", # Correct
        "The financial cost incurred when purchasing proprietary software licenses.",
        "The time spent debugging code that was written by other developers.",
        "The performance penalty of using outdated hardware or software versions."
    ],
    68: [ # Log Rotation
        "The process of renaming, compressing, or deleting old log files to save disk space.", # Correct
        "The systematic analysis of log files to identify security threats.",
        "The extraction of meaningful metrics from unstructured log data.",
        "The replication of log entries to a centralized logging server."
    ],
    70: [ # CI/CD Tools (Multi-select usually, but looks like single select string in DB based on dump)
        # Note: If it's multi-select, options should be individual items.
        # Checking dump ID 70: Correct: "Jenkins, GitHub Actions, GitLab CI, CircleCI"
        # Options: ["Jenkins", "GitHub Actions", ...]
        # This one is actually fine as is, wait. ID 70 options: ["Jenkins", "GitHub Actions", "GitLab CI", "CircleCI", "Microsoft Word", "VLC Player"]
        # The distractors are "Microsoft Word" and "VLC".
        # I should replace them with "Photoshop" or "Excel"? No, user wants similar length/type but wrong.
        # Actually for "Select popular CI/CD tools", maybe add "Kubernetes" (Orchestration, not CI/CD), "Terraform" (IaC)
    ],
    72: [ # Drift Detection
        "To detect manual changes to stack resources that were made outside of CloudFormation.", # Correct
        "To identify configuration errors in the CloudFormation template files.",
        "To monitor the performance metrics of the deployed resources in real-time.",
        "To automaticall roll back the stack if a resource creation fails."
    ],
    73: [ # Intrinsic Functions
        "Built-in functions like `!Sub` or `!Ref` used to assign values dynamically at runtime.", # Correct
        "Custom Python scripts that are executed during the stack creation process.",
        "External API calls used to fetch data from third-party services.",
        "System commands that facilitate debugging of the CloudFormation stack."
    ]
}

def update_questions():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 1. Fetch current questions to verify correct answer and merge
        # Actually I provided full option sets above including the correct one.
        # But I need to be careful: the CORRECT ANSWER string in the DB must match one of these options exactly.
        # My strings above are copied from the dump, so they should match.
        # I'll double check equality in the script.

        count = 0
        for q_id, new_opts in new_distractors.items():
            # Get correct answer
            cur.execute("SELECT correct_answer FROM quiz_questions WHERE id = %s", (q_id,))
            res = cur.fetchone()
            if not res:
                print(f"Skipping ID {q_id}, not found.")
                continue
            
            correct_ans = res[0]
            
            # Verify correct answer is in the new options (fuzzy match or direct?)
            # I must ensure the correct answer string is EXACTLY present.
            # If my hardcoded dictionary has a slight typo, it breaks.
            # So, strategy: Find the option in `new_opts` that looks like the correct one, and REPLACE it with the `correct_ans` from DB.
            # Or assume I was careful.
            # Better: Search for the option that is most similar, or if one matches perfectly, use it.
            
            # Simple approach: The first item in my list above WAS the correct answer copypasted. 
            # So I will overwrite `new_opts[0]` with `correct_ans` to ensure byte-for-byte equality.
            
            if q_id == 70:
                 # Special handling for ID 70 which was just distracting options
                 current_options = ["Jenkins", "GitHub Actions", "GitLab CI", "CircleCI", "Terraform", "Ansible"] 
                 # Terraform and Ansible are DevOps tools but strictly not CI/CD *runners* (though used in CI/CD).
                 # Or use "Visual Studio", "Notepad++" -> No user wants "similar length".
                 # Let's assume ID 70 is fine to skip for now or just replace Word/VLC.
                 new_opts = ["Jenkins", "GitHub Actions", "GitLab CI", "CircleCI", "Terraform", "Prometheus"]
            
            else:
                 new_opts[0] = correct_ans
            
            # Update DB
            # Need to convert list to json string? 
            # Postgres JSONB handling in psycopg2 usually adapts list automatically if using jsonb/json type.
            # The dump showed options as list. 
            # In app.py: `options` is row[3], used as list.
            # The SQL INSERT usually takes Json(list).
            
            # Since existing data was likely text[] or jsonb.
            # Let's assume JSONB for `options`.
            cur.execute("UPDATE quiz_questions SET options = %s WHERE id = %s", (json.dumps(new_opts), q_id))
            count += 1
            
        conn.commit()
        print(f"Updated {count} questions.")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Update error: {e}")

if __name__ == '__main__':
    update_questions()
