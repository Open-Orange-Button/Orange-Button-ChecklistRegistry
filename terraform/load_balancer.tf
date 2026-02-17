# The Application Load Balancer
resource "aws_lb" "main" {
  name               = "django-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.lb_sg.id]
  subnets            = module.vpc.public_subnets # Must be public for internet access
}

# Target Group for Django tasks
resource "aws_lb_target_group" "app" {
  name        = "django-tg"
  port        = 8000
  protocol    = "HTTP"
  vpc_id      = module.vpc.vpc_id
  target_type = "ip" # Required for Fargate

  health_check {
    path                = "/health/" # Or any standard Django endpoint
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

# Listener for HTTP traffic (Port 80)
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = "80"
  protocol          = "HTTP"
  depends_on        = [aws_lb_target_group.app]

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}
