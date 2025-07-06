terraform {
  backend "s3" {
    bucket       = "tao-weatherbits-terraform"
    key          = "dev/terraform.tfstate"
    region       = "eu-west-1"
    use_lockfile = true

  }
}

