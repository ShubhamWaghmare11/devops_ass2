variable "aws_region" {
  default = "ap-south-1"   # Mumbai
}

variable "instance_type" {
  default = "t2.micro"     # free-tier eligible
}

variable "docker_image" {
  description = "DockerHub image of FastAPI app"
  type        = string
}
