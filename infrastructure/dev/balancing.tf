resource "google_compute_global_address" "default" {
  name         = "ecommerce-ip"
  address_type = "EXTERNAL"
}


#resource "google_compute_managed_ssl_certificate" "ecommerce-ssl-cert" {
#  name = "ecommerce-ssl-cert"
#  managed {
#    domains = ["zahidgalea.com."]
#  }
#}
