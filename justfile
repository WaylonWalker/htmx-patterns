default:
  @just --list

build-image:
    podman build -t docker.io/waylonwalker/htmx-patterns-waylonwalker-com:$(hatch version) .

tag-wayl-one:
    podman tag docker.io/waylonwalker/htmx-patterns-waylonwalker-com:$(hatch version) registry.wayl.one/htmx-patterns-waylonwalker-com:latest
    podman tag docker.io/waylonwalker/htmx-patterns-waylonwalker-com:$(hatch version) registry.wayl.one/htmx-patterns-waylonwalker-com:$(hatch version)
push-wayl-one:
    podman push registry.wayl.one/htmx-patterns-waylonwalker-com:latest
    podman push registry.wayl.one/htmx-patterns-waylonwalker-com:$(hatch version)

push-image:
    podman push docker.io/waylonwalker/htmx-patterns-waylonwalker-com:$(hatch version)

shell:
    hatch shell

run:
    uv run htmx-patterns api run

lint:
    ruff format htmx_patterns
    ruff check --fix htmx_patterns


