default:
  @just --list

build-image:
    podman build -t docker.io/waylonwalker/htmx-patterns-waylonwalker-com:0.0.3 .

push-image:
    podman push docker.io/waylonwalker/htmx-patterns-waylonwalker-com:0.0.3

