resource "panos_ip_tag" "example1" {
    ip = "10.2.3.4"
    tags = [
        "Automation",
    ]

    lifecycle {
        create_before_destroy = true
    }
}
