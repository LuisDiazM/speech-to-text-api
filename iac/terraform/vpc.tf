resource "digitalocean_vpc" "speech-to-text-vpc" {
  name     = "network-speech"
  region   = "nyc1"
}