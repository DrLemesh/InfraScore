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

resource "aws_subnet" "infrascore_subnet" {
  vpc_id     = aws_vpc.infrascore_vpc.id
  cidr_block = "10.0.1.0/24"

  tags = {
    Name = "infrascore-subnet"
  }
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

# קישור הטבלה לסאבנט שיצרת קודם
resource "aws_route_table_association" "infrascore_rta" {
  subnet_id      = aws_subnet.infrascore_subnet.id
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
