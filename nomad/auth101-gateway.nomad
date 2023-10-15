job "auth101-gateway" {
    datacenters = ["*"]
    type = "service"

    group "app" {
    
    count = 1

    network {
      port "http" {
        to = 8080
      }
    }

    service {
      name     = "auth101-gateway-svc"
      tags     = ["global", "auth101"]
      port     = "http"
      provider = "nomad"

    }

    task "auth101-gw-app" {

      driver = "docker"

      config {
        image = "mebaysan/auth101-gateway"
        ports = ["http"]
      }

      env {
        AUTH_SERVICE_URL = "http://172.17.0.2:5000"
      }

# We can use "range nomadService" to get the service address and port
//      template {
//         data        = <<EOH
// {{ range nomadService "auth101-auth-svc" }}
// AUTH_SERVICE_URL=http://{{ .Address }}:{{ .Port }}
// {{ end }}
// EOH
//         destination = "local/env.txt"
//         env         = true
//       }

    }
  }
}