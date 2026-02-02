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
