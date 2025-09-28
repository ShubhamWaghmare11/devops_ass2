# Security Group to allow port 8000
resource "aws_security_group" "fastapi_sg" {
  name        = "fastapi-sg"
  description = "Allow HTTP on port 8000"

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Fetch latest Ubuntu AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

# EC2 instance
resource "aws_instance" "fastapi_ec2" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
  vpc_security_group_ids = [aws_security_group.fastapi_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              sudo apt update
              sudo apt install -y docker.io
              sudo systemctl start docker
              sudo systemctl enable docker
              sudo docker run -d -p 8000:8000 shubhamwaghmare11/devopsass2:latest
              EOF

  tags = {
    Name = "FastAPI-Terraform"
  }
}

# Output public IP
output "fastapi_public_ip" {
  value = aws_instance.fastapi_ec2.public_ip
}
