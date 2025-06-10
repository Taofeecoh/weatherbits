terraform {
  backend "s3" {
    bucket       = "tao-weatherbits-terraform"
    key          = "dev/terraform.tfstate"
    region       = "us-east-2"
    use_lockfile = true

  }
}

