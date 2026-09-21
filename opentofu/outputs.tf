output "control_plane_ip" {
  value       = "203.0.113.10"
  description = "Control plane IP placeholder"
}

output "node_count_provisioned" {
  value       = var.node_count
  description = "Provisioned node count"
}
