# Docker example with NginX + Auth-Request module proxying to auth-acting Django server for Shiny app
This is a [Docker][] setup for a [Django] application acting as an authentication
and authorization server for a [Shiny] application, through the [NginX][]
reverse-proxy and [auth-request][] module.

- We use [NginX][] as reverse proxy.
- We use [auth-request][] module to add an authorization step for each request
  directed to Shiny.
- The initial [Shiny][] application main page is wrapped into a
  [Django][]-powered page, so we can build an interface above [Shiny][],
  with user and access rights management.

A [Makefile][] is available for convenience. You might need to use `sudo make`
instead of just `make` because `docker` and `docker-compose` commands often needs
admin privilege.

## Requirements
You need to install [Docker][] and [Docker-Compose][].

## Build
`sudo make all`.

## Run
`sudo make up`.

## Help
`make` or `make help`.

[auth-request]: https://nginx.org/en/docs/http/ngx_http_auth_request_module.html
[Docker]: https://www.docker.com/
[Django]: https://www.djangoproject.com/
[NginX]: https://www.nginx.com/
[Makefile]: https://www.gnu.org/software/make/manual/make.html
[Docker-Compose]: https://docs.docker.com/compose/
[Shiny]: https://shiny.rstudio.com/
