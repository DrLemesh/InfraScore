provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "infrascore_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "infrascore-vpc"
  }
}

resource "aws_subnet" "infrascore_subnet_1" {
  vpc_id                  = aws_vpc.infrascore_vpc.id
  availability_zone       = "us-east-1a"
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name = "infrascore-subnet"
  }
}
resource "aws_subnet" "infrascore_subnet_2" {
  vpc_id                  = aws_vpc.infrascore_vpc.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "us-east-1b" # אזור ב' - חשוב שיהיה שונה!
  map_public_ip_on_launch = true
}
resource "aws_internet_gateway" "infrascore_igw" {
  vpc_id = aws_vpc.infrascore_vpc.id

  tags = {
    Name = "infrascore-igw"
  }
}
resource "aws_route_table" "infrascore_rt" {
  vpc_id = aws_vpc.infrascore_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.infrascore_igw.id
  }

  tags = {
    Name = "infrascore-rt"
  }
}

# קישור הטבלה לסאבנט 1
resource "aws_route_table_association" "infrascore_rta" {
  subnet_id      = aws_subnet.infrascore_subnet_1.id
  route_table_id = aws_route_table.infrascore_rt.id
}

# קישור הטבלה לסאבנט 2 (התיקון)
resource "aws_route_table_association" "infrascore_rta_2" {
  subnet_id      = aws_subnet.infrascore_subnet_2.id
  route_table_id = aws_route_table.infrascore_rt.id
}

# ECR Repositories

# Backend Repository
resource "aws_ecr_repository" "infrascore_backend" {
  name                 = "infrascore-backend"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# Frontend Repository
resource "aws_ecr_repository" "infrascore_frontend" {
  name                 = "infrascore-frontend"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# 1. התפקיד של הקלאסטר (המוח)
resource "aws_iam_role" "eks_cluster_role" {
  name = "infrascore-eks-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "eks.amazonaws.com"
      }
    }]
  })
}

# 2. חיבור הפוליסה לתפקיד הקלאסטר
resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks_cluster_role.name
}

# 3. התפקיד של השרתים (הפועלים)
resource "aws_iam_role" "eks_nodes_role" {
  name = "infrascore-eks-nodes-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

# 4. חיבור הפוליסות לשרתים (Nodes)
resource "aws_iam_role_policy_attachment" "eks_worker_node_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.eks_nodes_role.name
}

resource "aws_iam_role_policy_attachment" "eks_ecr_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.eks_nodes_role.name
}

resource "aws_iam_role_policy_attachment" "eks_cni_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.eks_nodes_role.name
}
resource "aws_eks_cluster" "infrascore_cluster" {
  name     = "infrascore-eks"
  role_arn = aws_iam_role.eks_cluster_role.arn # ה-Role שיצרנו אתמול

  vpc_config {
    subnet_ids = [aws_subnet.infrascore_subnet_1.id,
    aws_subnet.infrascore_subnet_2.id] # הסאבנט שיצרת בהתחלה
  }

  # וודא שהקלאסטר נוצר רק אחרי שה-Role והפוליסות מוכנים
  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_policy
  ]
}
resource "aws_eks_node_group" "infrascore_nodes" {
  cluster_name    = aws_eks_cluster.infrascore_cluster.name
  node_group_name = "infrascore-node-group"
  node_role_arn   = aws_iam_role.eks_nodes_role.arn # ה-Role של השרתים
  subnet_ids = [aws_subnet.infrascore_subnet_1.id,
  aws_subnet.infrascore_subnet_2.id]

  scaling_config {
    desired_size = 2 # כמה שרתים תמיד יהיו באוויר
    max_size     = 3
    min_size     = 1
  }

  instance_types = ["t3.medium"] # סוג השרת (medium מומלץ ל-EKS, micro קטן מדי)

  depends_on = [
    aws_iam_role_policy_attachment.eks_worker_node_policy,
    aws_iam_role_policy_attachment.eks_ecr_policy,
    aws_iam_role_policy_attachment.eks_cni_policy
  ]
}
