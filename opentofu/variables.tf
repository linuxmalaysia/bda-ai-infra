variable "environment" {
  type        = string
  default     = "staging"
  description = "Target deployment environment"
}

variable "node_count" {
  type        = number
  default     = 3
  description = "Number of worker nodes"
}
