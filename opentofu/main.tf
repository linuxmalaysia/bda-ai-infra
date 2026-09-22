# Sovereign Infrastructure Fabric - OpenTofu Main Configuration

terraform {
  required_version = ">= 1.6.0"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4.0"
    }
  }
}

provider "local" {}

resource "local_file" "ansible_inventory_matrix" {
  filename = "${path.module}/../playbooks/inventory/generated_hosts.ini"
  content  = <<EOT
[control_plane]
control-01.internal.example.org ansible_host=203.0.113.10

[worker_nodes]
%{ for i in range(1, var.node_count + 1) ~}
node-0${i}.internal.example.org ansible_host=203.0.113.${10 + i}
%{ endfor ~}

[all:vars]
environment=${var.environment}
ansible_user=sysadmin
ansible_python_interpreter=/usr/bin/python3
EOT
}
