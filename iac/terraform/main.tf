resource "digitalocean_kubernetes_cluster" "speech-cluser-k8s" {
  name   = "speech-cluster"
  region = "nyc1"
  version = "1.30.1-do.0"
  vpc_uuid = digitalocean_vpc.speech-to-text-vpc.id

  node_pool {
    name       = "worker-pool"
    size       = "s-2vcpu-2gb"
    auto_scale = true
    min_nodes  = 1
    max_nodes  = 3

    taint {
      key    = "workloadKind"
      value  = "database"
      effect = "NoSchedule"
    }
  }
}