default:
  @just --list

build-image:
    podman build -t docker.io/waylonwalker/htmx-patterns-waylonwalker-com:$(hatch version) .

push-image:
    podman push docker.io/waylonwalker/htmx-patterns-waylonwalker-com:$(hatch version)


