terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "default"
  region  = "eu-central-1"
}

resource "aws_instance" "app_server" {
  ami             = "ami-0277b52859bac6f4b"
  instance_type   = "t2.micro"
  key_name        = "TestLinuxServer"
  user_data	= file("instructions.sh")
  security_groups = [ "Docker" ]

  tags = {
    Name = "BloomreachApiApp"
  }
}

resource "aws_security_group" "Docker" {
  tags = {
    type = "terraform-security-group"
  }
}