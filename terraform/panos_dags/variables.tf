/* Firewall Connectivity -------------------------------------------------- */

variable "firewall" {
  description = "Firewall connection details"
  type = object({
    fw_ip    = string,
    username = string,
    password = string,
  })
}

