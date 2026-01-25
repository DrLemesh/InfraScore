import json
import os
import glob
import psycopg2

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        database=os.environ.get('DB_NAME', 'quiz_project'),
        user=os.environ.get('DB_USER', 'admin'),
        password=os.environ.get('DB_PASSWORD', 'password123')
    )

# Map of "Question Text Substring" -> [New Distractors (excluding correct one usually, or full list)]
# Strategy: I will provide a list of 3 distractors. The script will find the question, keep the correct answer, and replace the OTHER options with these 3.
# This ensures strict length balancing.

fixes = {
    "What is an 'SLA' (Service Level Agreement)?": [
        "A formal specification defining the API endpoints and data formats for a microservice.",
        "A strict security protocol that governs how data is encrypted in transit and at rest.",
        "A marketing document that outlining the theoretical maximum performance of a product."
    ],
    "What is 'Chaos Monkey'?": [
        "A specialized fuzzer that injects random operational codes into running binaries to find overflow bugs.",
        "A load testing script that generates unpredictable traffic spikes to stress test auto-scaling groups.",
        "A monitoring agent that randomly polls services to check for intermittent network latency issues."
    ],
    "What distinguishes a Docker Volume from a Bind Mount?": [
        "Volumes are strictly read-only and immutable, while Bind Mounts allow for read-write access to host files.",
        "Bind Mounts offer higher I/O performance than Volumes because they bypass the Docker storage driver completely.",
        "Volumes are only supported on Linux hosts, whereas Bind Mounts are the only option for Windows containers."
    ],
    "What is the primary definition of DevOps?": [
        "A specific set of software tools including Jenkins and Docker used to automate deployment pipelines.",
        "A job title for engineers who are responsible for maintaining physical server hardware and cabling.",
        "A strict project management methodology that replaces Agile with a linear Waterfall approach."
    ],
    "What is a 'Hybrid Cloud' environment?": [
        "A network architecture that uses both IPv4 and IPv6 protocols simultaneously for internet connectivity.",
        "A system that runs on both Windows and Linux servers within the same physical data center.",
        "A storage solution that combines solid-state drives (SSD) with traditional hard disk drives (HDD) for speed."
    ],
    "What is the purpose of an 'API Gateway'?": [
        "It serves as a firewall that blocks all incoming traffic unless it originates from a trusted IP address.",
        "It is a database caching layer that stores frequently accessed records to reduce query load on the backend.",
        "It is a dedicated server that encrypts all user passwords before they are stored in the primary database."
    ],
    "What is a 'Sidecar' in Kubernetes?": [
        "A redundant replica of the main Pod that automatically takes over if the primary container crashes.",
        "A storage volume that is shared between all Pods on a specific Node for temporary file exchange.",
        "A network policy that restricts traffic flow between different Namespaces within the cluster."
    ],
    "What is the 'Twelve-Factor App' methodology?": [
        "A strict agile framework that requires teams to have exactly twelve members for optimal efficiency.",
        "A coding standard that limits functions to twelve lines of code to ensure readability and maintainability.",
        "A security protocol that mandates twelve distinct layers of encryption for user data protection."
    ],
    "What is an 'Approval Stage'?": [
        "A fully automated testing phase that runs a suite of unit tests before merging code to the main branch.",
        "A code review process where developers must get signs-off from three peers before committing changes.",
        "A security scan that checks for vulnerabilities in third-party libraries and dependencies automatically."
    ],
    "What is an 'SLO' (Service Level Objective)?": [
        "A legally binding contract that specifies financial penalties if the service availability drops below 100%.",
        "A subjective measure of user satisfaction gathered through quarterly surveys and feedback forms.",
        "A technical document describing the architecture and design patterns used in the microservice."
    ],
    "What is a 'Self-Hosted Runner'?": [
        "A cloud-based virtual machine automatically provisioned by GitHub to run your actions workflows.",
        "A containerized agent that runs exclusively on the developer's local laptop for debugging purposes.",
        "A deprecated CI/CD component that has been replaced by serverless lambda functions in modern pipelines."
    ],
    "What is 'Containerization'?": [
        "Virtualizing the entire hardware stack to run multiple operating systems on a single physical server.",
        "Compressing large files into smaller archives to save disk space during network transfers.",
        "Encrypting application data to ensure it remains secure while stored in public cloud buckets."
    ],
    "What is a primary difference between Docker Swarm and Kubernetes?": [
        "Docker Swarm is designed for stateful applications, while Kubernetes can only handle stateless microservices.",
        "Kubernetes is a single-node tool for local development, while Swarm is for multi-region clusters.",
        "Docker Swarm uses a declarative YAML syntax, whereas Kubernetes relies entirely on imperative CLI commands."
    ],
    "What is an 'Automated Rollback'?": [
        "A database backup process that runs every night to ensure data is preserved in case of corruption.",
        "A manual procedure where an admin logs in to restart servers when performance degrades.",
        "A feature that prevents developers from merging broken code into the main repository branch."
    ],
    "What is 'YAGNI'?": [
        "Yet Another Graphical Interface - a design pattern prioritizing visual aesthetics over functionality.",
        "Your Application Goes Nowhere Instantly - a warning about poor performance in infinite loops.",
        "Yield All Generated New Instances - a memory management technique for garbage collection."
    ],
    "How do 'Monorepos' challenge CI/CD pipelines?": [
        "They force developers to use a single programming language for all projects in the repository.",
        "They make it impossible to use version control systems like Git due to file size limits.",
        "They require manual deployment of every service whenever a single line of code is changed anywhere."
    ],
    "What is 'Pipeline as Code'?": [
        "Writing the application source code entirely within the CI/CD configuration tool's web editor.",
        "A graphical drag-and-drop interface for building deployment workflows without writing scripts.",
        "Compiling the pipeline configuration into a binary executable for faster execution speed."
    ],
    "What is 'FinOps' in the context of cloud computing?": [
        "A technical role focused solely on optimizing the memory usage of Java applications to save RAM.",
        "A rigorous security auditing process to ensure financial data is encrypted at rest.",
        "A deployment strategy that prioritizes finishing operations quickly regardless of resource cost."
    ],
    "What is Site Reliability Engineering (SRE)?": [
        "A traditional help-desk role focused on resolving user password resets and hardware issues.",
        "A software development methodology that ignores operational concerns to maximize feature velocity.",
        "A pure hardware engineering discipline focused on designing more efficient server racks and cooling."
    ],
    "What is 'Edge Computing'?": [
        "Centralizing all data processing in a single massive supercomputer to maximize raw performance.",
        "Running all computations on the user's web browser to offload work from the server completely.",
        "Using cutting-edge experimental hardware that has not yet been released to the general public."
    ],
    "What is Infrastructure as Code (IaC)?": [
        "Writing comprehensive text documentation to describe how to manually configure servers.",
        "Using physical hardware switches to route network traffic instead of software-defined networking.",
        "Developing software applications that manage their own memory allocation directly."
    ],
    "How do you secure secrets in DevOps?": [
        "Hardcode them in the source code but use complex variable names to hide them from search.",
        "Store them in a shared Google Doc accessible only to the development team members.",
        "Encrypt them locally and email the decryption keys to the operations team before deployment."
    ],
    "Why use multi-stage builds in Docker?": [
        "To allow a single container to run multiple different operating systems simultaneously.",
        "To increase the build speed by downloading all dependencies from a local cache server.",
        "To enable the Docker container to access the host machine's full filesystem directly."
    ],
    "What function does a 'Service Mesh' (like Istio) perform?": [
        "It acts as a distributed database for storing user session data across multiple regions.",
        "It compiles microservices into a single monolithic binary for easier deployment.",
        "It automatically rewrites application code to be more efficient and performant."
    ],
    "What is 'Infrastructure Testing'?": [
        "Manually logging into every server to check if the operating system is up to date.",
        "Running stress tests on the physical hardware to ensure the CPUs do not overheat.",
        "Checking if the office Wi-Fi is fast enough to support the development team's needs."
    ],
    "What is an 'Ephemeral Build Environment'?": [
        "A dedicated physical server that is kept running 24/7 to ensure build consistency.",
        "A developer's local laptop that is used to run production builds for the final release.",
        "A shared staging environment where all developers deploy their changes manually."
    ],
    "Why is a 'Staging Environment' important?": [
        "It provides a place for developers to test disruptive experimental features directly on live user data.",
        "It serves as a permanent backup of the production environment in case of catastrophic failure.",
        "It is used to demo the product to potential investors who need to see a perfect version."
    ],
    "How should Environment Variables be handled in CI/CD?": [
        "They should be committed directly to the Git repository in a cleartext config file for easy access.",
        "They should be hardcoded into the application binary to prevent them from being changed accidentally.",
        "They should be emailed to the system administrator who manually types them in during deployment."
    ],
    "How does a 'Feature Flag' assist in CI/CD?": [
        "It flags code that contains potential bugs so the compiler knows to skip it during the build.",
        "It marks a specific commit as a 'feature' so it can be tracked in the release notes automatically.",
        "It prevents developers from pushing code to the repository if it hasn't been reviewed yet."
    ],
    "What is 'Continuous Testing'?": [
        "A manual testing phase that occurs once at the end of the project before the final release.",
        "Running the application in a loop to see if it crashes after 24 hours of uptime.",
        "Asking beta testers to use the app continuously and report valid bugs via email."
    ],
    "What is 'Continuous Delivery'?": [
        "A process where every change is deployed to production immediately without any manual approval.",
        "A logistics term referring to the uninterrupted shipping of physical hardware components.",
        "writing code continuously without stopping for breaks to ensure maximum productivity."
    ],
    "What is 'Federated Identity'?": [
        "A centralized database that stores every user's password in a single plaintext file.",
        "A requirement for all users to have a government-issued ID card to access the system.",
        "A feature that forces users to change their username every 30 days for security."
    ],
    "Why use 'Microservices'?": [
        "To consolidate all code into a single massive file for easier searching and editing.",
        "To ensure that all components of the application rely on the exact same database schema.",
        "To simplify the deployment process by having only one artifact to manage and monitor."
    ],
    "How does DevOps relate to Agile?": [
        "DevOps is a replacement for Agile, arguing that speed is more important than iteration.",
        "Agile focuses on hardware development, while DevOps focuses exclusively on software.",
        "They are competing methodologies that cannot be used together in the same organization."
    ],
    "What is a 'Provider' in Terraform?": [
        "The internet service provider (ISP) that gives the server connectivity to the web.",
        "The developer who is responsible for providing the code for a specific module.",
        "A specific type of text file that lists the variables used in the configuration."
    ],
    "What is a 'DMZ' in network security?": [
        "A highly secure internal zone where critical databases are stored offline.",
        "A specific firewall rule that blocks all traffic from specific countries.",
        "A software patch that removes vulnerabilities from the operating system kernel."
    ],
    "What does an SBOM (Software Bill of Materials) provide?": [
        "A financial invoice detailing the cost of all software licenses purchased.",
        "A list of all developers who contributed code to the project.",
        "A marketing checklist of all the features included in the release."
    ],
    "How does 'Auto-Remediation' work?": [
        "It uses AI to automatically write code fixes for bugs found during testing.",
        "It automatically emails the developer who broke the build to tell them to fix it.",
        "It shuts down the entire system to prevent damage whenever an error occurs."
    ],
    "What is 'Dependency Hell'?": [
        "A situation where developers rely too much on StackOverflow for answers.",
        "A strict manager who forces developers to work dependent on their approval.",
        "A database schema that has too many foreign key constraints."
    ],
    "What is 'Progressive Delivery'?": [
        "Delivering the software on a physical disk to the customer via courier.",
        "Focusing on delivering the most complex features first before the basics.",
        "Ignoring backward compatibility to force users to upgrade immediately."
    ],
    "What is 'Distributed Tracing'?": [
        "A technique for physically locating the servers in a datacenter using GPS.",
        "A security audit that traces the IP address of hackers back to their source.",
        "A method of backing up data to multiple hard drives in different locations."
    ],
    "What is 'Feedback Loop' in DevOps?": [
        "A coding error where a function calls itself infinitely until it crashes.",
        "A hardware issue where microphone audio is played back through the speakers.",
        "A weekly meeting where managers give feedback to their subordinates."
    ],
    "What is Prometheus?": [
        "A relational database management system designed for transactional workloads.",
        "A proprietary visualization tool that requires a paid license for every user.",
        "A CI/CD orchestrator widely used for managing Jenkins pipelines."
    ],
    "Why is 'Artifact Versioning' crucial?": [
        "It ensures that filenames are unique so that they don't overwrite each other on the desktop.",
        "It allows marketing to give cool names like 'Tiger' or 'Lion' to software releases.",
        "It is a legal requirement for copyrighting the software code."
    ],
    "What does running CI/CD 'inside containers' achieve?": [
        "It allows the build to run faster by using the host machine's full resources.",
        "It prevents the build process from accessing the internet for security reasons.",
        "It ensures the build runs on a physical server rather than a virtual one."
    ],
    "What is 'MVP' (Minimum Viable Product)?": [
        "The most valuable player on the development team who writes the most code.",
        "The maximum feature set that can possibly be built within the budget.",
        "A fully polished product with no bugs, ready for mass market adoption."
    ]
}

def apply_fixes():
    # 1. Update Files
    dataset_files = glob.glob('database/datasets/datasets/*.json')
    for fpath in dataset_files:
        with open(fpath, 'r') as f:
            try:
                data = json.load(f)
                if not isinstance(data, list): continue
                
                updated = False
                new_data = []
                
                for q in data:
                    q_text = q.get('question_text') or q.get('question')
                    
                    # Remove "Answer:" or broken questions
                    if q_text and (q_text.strip() == "Answer:" or len(q_text) < 5):
                         updated = True
                         continue # skip this question
                         
                    # Check for fix
                    matched_key = None
                    for k in fixes.keys():
                        if k in q_text: # Loose matching title
                            matched_key = k
                            break
                    
                    if matched_key:
                        new_distractors = fixes[matched_key]
                        correct = q.get('correct_answer')
                        
                        # Set new options: Correct + New Distractors
                        all_options = [correct] + new_distractors
                        q['options'] = all_options 
                        updated = True
                    
                    new_data.append(q)
                
                if updated:
                    with open(fpath, 'w') as outf:
                        json.dump(new_data, outf, indent=2)
                        print(f"Updated {fpath}")
                        
            except Exception as e:
                print(f"Error reading {fpath}: {e}")

    # 2. Update Database
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        count = 0
        for q_text_key, distractors in fixes.items():
            # Find questions in DB matching loosely
            cur.execute("SELECT id, correct_answer FROM quiz_questions WHERE question_text LIKE %s", (f"%{q_text_key}%",))
            rows = cur.fetchall()
            
            for row in rows:
                qid, correct = row
                all_opts = [correct] + distractors
                
                cur.execute("UPDATE quiz_questions SET options = %s WHERE id = %s", (json.dumps(all_opts), qid))
                count += 1
                
        conn.commit()
        print(f"Updated {count} questions in database.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"DB Error: {e}")

if __name__ == '__main__':
    apply_fixes()
