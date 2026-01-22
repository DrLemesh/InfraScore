
import psycopg2
import os
import json

def seed_database():
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get('POSTGRES_DB', 'quiz_project'),
            user=os.environ.get('POSTGRES_USER', 'admin'),
            password=os.environ.get('POSTGRES_PASSWORD', 'password123'),
            host=os.environ.get('POSTGRES_HOST', 'db'),
            port=os.environ.get('POSTGRES_PORT', '5432')
        )
        cur = conn.cursor()
        
        # Create quiz_questions table
        print("Creating quiz_questions table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS quiz_questions (
                id SERIAL PRIMARY KEY,
                question_text TEXT NOT NULL,
                question_type VARCHAR(50) NOT NULL,
                options JSONB,
                correct_answer TEXT,
                difficulty_level INTEGER,
                category VARCHAR(100),
                reference_answer TEXT,
                estimated_minutes INTEGER,
                tags JSONB
            );
        """)
        
        # Check if table is empty
        cur.execute("SELECT count(*) FROM quiz_questions;")
        count = cur.fetchone()[0]
        
        if count > 0:
            print(f"Table already has {count} questions. Skipping seed.")
            return

        # Sample questions
        questions = [
            # Level 1 (Junior)
            {
                "question_text": "Which command is used to list all running Docker containers?",
                "question_type": "multiple_choice",
                "options": ["docker ps", "docker list", "docker run", "docker images"],
                "correct_answer": "docker ps",
                "difficulty_level": 1,
                "category": "Docker",
                "reference_answer": "The 'docker ps' command lists all running containers. Adding '-a' lists all containers including stopped ones."
            },
            {
                "question_text": "What does CI/CD stand for?",
                "question_type": "multiple_choice", 
                "options": ["Continuous Integration/Continuous Deployment", "Code Integration/Code Deployment", "Cloud Integration/Cloud Deployment", "Computer Integration/Computer Delivery"],
                "correct_answer": "Continuous Integration/Continuous Deployment",
                "difficulty_level": 1,
                "category": "DevOps Concepts",
                "reference_answer": "CI/CD stands for Continuous Integration and Continuous Deployment (or Delivery)."
            },
             {
                "question_text": "Which HTTP method is typically used to retrieve data?",
                "question_type": "multiple_choice",
                "options": ["GET", "POST", "PUT", "DELETE"],
                "correct_answer": "GET",
                "difficulty_level": 1,
                "category": "Networking",
                "reference_answer": "GET is the standard HTTP method for retrieving resources."
            },
            
            # Level 3 (DevOps/Mid)
            {
                "question_text": "In Kubernetes, which object ensures a specified number of pod replicas are running at any given time?",
                "question_type": "multiple_choice",
                "options": ["ReplicaSet", "Pod", "Service", "Ingress"],
                "correct_answer": "ReplicaSet",
                "difficulty_level": 3,
                "category": "Kubernetes",
                "reference_answer": "A ReplicaSet's purpose is to maintain a stable set of replica Pods running at any given time."
            },
            {
                "question_text": "Select all components that are part of the Kubernetes Control Plane.",
                "question_type": "multi_select",
                "options": ["etcd", "kube-scheduler", "kubelet", "kube-apiserver", "kube-proxy"],
                "correct_answer": ["etcd", "kube-scheduler", "kube-apiserver"],
                "difficulty_level": 3,
                "category": "Kubernetes",
                "reference_answer": "Control Plane components include kube-apiserver, etcd, kube-scheduler, and kube-controller-manager. Kubelet and kube-proxy run on worker nodes."
            },
            {
                "question_text": "Which Terraform command creates an execution plan?",
                "question_type": "multiple_choice",
                "options": ["terraform plan", "terraform apply", "terraform init", "terraform validate"],
                "correct_answer": "terraform plan",
                "difficulty_level": 3,
                "category": "Terraform",
                "reference_answer": "The 'terraform plan' command creates an execution plan, letting you preview the changes Terraform plans to make to your infrastructure."
            },
             {
                "question_text": "What is the primary function of a reverse proxy?",
                "question_type": "open_ended",
                "options": [],
                "correct_answer": "",
                "difficulty_level": 3,
                "category": "Networking",
                "reference_answer": "A reverse proxy sits in front of web servers and forwards client requests to those web servers. It provides load balancing, improved security, and caching."
            },
            
            # Level 5 (Senior/Principal)
            {
                "question_text": "Explain the concept of 'GitOps' and its primary benefits.",
                "question_type": "open_ended",
                "options": [],
                "correct_answer": "",
                "difficulty_level": 5,
                "category": "DevOps Methodology",
                "reference_answer": "GitOps is a set of practices to manage infrastructure and application configurations using Git. It uses Git as a single source of truth for declarative infrastructure and applications."
            },
            {
                "question_text": "Which of the following are valid strategies for Zero Downtime Deployment?",
                "question_type": "multi_select",
                "options": ["Blue-Green Deployment", "Canary Deployment", "Rolling Update", "Recreate Deployment"],
                "correct_answer": ["Blue-Green Deployment", "Canary Deployment", "Rolling Update"],
                "difficulty_level": 5,
                "category": "Deployment Strategies",
                "reference_answer": "Blue-Green, Canary, and Rolling Updates allow for zero downtime. 'Recreate' strategy involves downtime as it terminates old pods before creating new ones."
            },
            {
                "question_text": "In a distributed system, what does the CAP theorem state you can only have two of?",
                "question_type": "multiple_choice",
                "options": ["Consistency, Availability, Partition Tolerance", "Consistency, Accuracy, Performance", "Concurrency, Availability, Performance", "Consistency, Authenticity, Partition Tolerance"],
                "correct_answer": "Consistency, Availability, Partition Tolerance",
                "difficulty_level": 5,
                "category": "System Design",
                "reference_answer": "CAP theorem states that a distributed data store can only provide two of the following three guarantees: Consistency, Availability, and Partition Tolerance."
            }
        ]
        
        # Add more Level 3 questions to ensure we have enough for the quiz
        level_3_extras = [
            
            {
                "question_text": "What is the difference between a Container and a Virtual Machine?",
                "question_type": "open_ended",
                "options": [],
                "correct_answer": "",
                "difficulty_level": 3,
                "category": "Containers",
                "reference_answer": "Containers share the host OS kernel and are lightweight, while VMs have their own full OS and are heavier."
            },
            {
                "question_text": "Which command checks the status of a systemd service?",
                "question_type": "multiple_choice",
                "options": ["systemctl status <service>", "service <service> status", "ps -ef | grep <service>", "All of the above"],
                "correct_answer": "systemctl status <service>",
                "difficulty_level": 3,
                "category": "Linux",
                "reference_answer": "While others might give info, 'systemctl status' is the standard command for checking systemd service status."
            },
            {
                "question_text": "What is the purpose of Docker Compose?",
                "question_type": "multiple_choice",
                "options": ["To define and run multi-container Docker applications", "To build Docker images", "To push images to Docker Hub", "To orchestrate containers across multiple hosts"],
                "correct_answer": "To define and run multi-container Docker applications",
                "difficulty_level": 3,
                "category": "Docker",
                "reference_answer": "Docker Compose is a tool for defining and running multi-container Docker applications using a YAML file."
            },
             {
                "question_text": "Which port is the default for SSH?",
                "question_type": "multiple_choice",
                "options": ["22", "80", "443", "21"],
                "correct_answer": "22",
                "difficulty_level": 3,
                "category": "Networking",
                "reference_answer": "Port 22 is the standard default port for SSH."
            },
            {
                "question_text": "What is 'Infrastructure as Code' (IaC)?",
                "question_type": "multiple_choice",
                "options": ["Managing infrastructure using code and config files", "Writing code to build physical servers", "Installing OS manually", "None of the above"],
                "correct_answer": "Managing infrastructure using code and config files",
                "difficulty_level": 3,
                "category": "DevOps Concepts",
                "reference_answer": "IaC is the process of managing and provisioning computer data centers through machine-readable definition files, rather than physical hardware configuration or interactive configuration tools."
            },
             {
                "question_text": "Which of these is NOT a valid HTTP status code category?",
                "question_type": "multiple_choice",
                "options": ["6xx", "2xx", "4xx", "5xx"],
                "correct_answer": "6xx",
                "difficulty_level": 3,
                "category": "Networking",
                "reference_answer": "Standard HTTP status codes are in the ranges 1xx, 2xx, 3xx, 4xx, and 5xx."
            },
             {
                "question_text": "What is a 'DaemonSet' in Kubernetes?",
                "question_type": "multiple_choice",
                "options": ["Ensures copy of pod runs on all (or some) nodes", "Manages stateful applications", "Runs a job to completion", "Exposes a service"],
                "correct_answer": "Ensures copy of pod runs on all (or some) nodes",
                "difficulty_level": 3,
                "category": "Kubernetes",
                "reference_answer": "A DaemonSet ensures that all (or some) Nodes run a copy of a Pod."
            },
            {
                "question_text": "Which Linux command is used to change file permissions?",
                "question_type": "multiple_choice",
                "options": ["chmod", "chown", "chgrp", "umask"],
                "correct_answer": "chmod",
                "difficulty_level": 3,
                "category": "Linux",
                "reference_answer": "chmod (change mode) is used to change the access permissions of file system objects."
            }
        ]
        
        questions.extend(level_3_extras)

        print(f"Seeding {len(questions)} questions...")
        
        for q in questions:
            cur.execute("""
                INSERT INTO quiz_questions 
                (question_text, question_type, options, correct_answer, difficulty_level, category, reference_answer, estimated_minutes, tags)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                q['question_text'],
                q['question_type'],
                json.dumps(q['options']),
                json.dumps(q['correct_answer']) if isinstance(q['correct_answer'], list) else q['correct_answer'],
                q['difficulty_level'],
                q['category'],
                q['reference_answer'],
                2, # estimated minutes
                json.dumps(["devops", q['category'].lower()])
            ))
        
        conn.commit()
        print("Database seeded successfully!")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error seeding database: {e}")

if __name__ == "__main__":
    seed_database()
