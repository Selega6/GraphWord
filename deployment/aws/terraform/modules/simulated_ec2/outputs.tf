output "simulated_ec2_container_id" {
  description = "ID del contenedor que simula EC2"
  value       = docker_container.simulated_ec2.id
}

output "simulated_ec2_ip" {
  description = "IP estática de la EC2 simulada"
  value       = tolist([for net in docker_container.simulated_ec2.networks_advanced : net.ipv4_address])[0]
}

output "simulated_ec2_api_url" {
  description = "URL de acceso al API alojado en la EC2 simulada"
  value       = "http://localhost:8080"
}

