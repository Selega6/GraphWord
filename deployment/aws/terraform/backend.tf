terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 2.23.0"
    }
  }
  backend "local" {
    path = "terraform.tfstate"
  }
}
