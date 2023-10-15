job "auth101-auth" {
    datacenters = ["*"]
    type = "service"

    group "app" {
        count = 1

        network {
            port "http" {
                to = 5000
            }
        }

        service {
            name     = "auth101-auth-svc"
            tags     = ["global", "auth101"]
            port     = "http"
            provider = "nomad"
            
        }

        task "auth101-auth-app" {
            driver = "docker"

            config {
                image = "mebaysan/auth101-auth"
                ports = ["http"]
            }

            env {
                JWT_SECRET = "Th1s1sV3ryS3cr3tK3y!."
            }

            resources {
                cpu    = 500
                memory = 256
            }

        }
    }
}
