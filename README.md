# Description
See [tech_tests folder](tech_tests) for tests content

# Prerequisites
## Scripting utility : task
```bash
# if not using a mac, search for your platform installation method
brew install go-task/tap/go-task
```
## Project dependencies
Only needed to commit to this project, not needed to run it
```bash
task install-dependencies
```
## IDE Configuration
Only needed to commit to this project, not needed to run it
### black
[Configure it for your IDE](https://black.readthedocs.io/en/stable/integrations/editors.html)

Please keep your version of black always up-to-date (`pip install black -U` to upgrade)

# How to run
## Preparation
```shell
cd buildrun/docker/docker-compose/dev-env
# init the app
# This should be called only the first time you run the app or if you want to reset everything
task init-app
```
## App run
```shell
# Run the app after first initialisation (it is advised to set up your IDE to run the app instead)
task up
```
## Pycharm setup
Set project interpreter to a docker-compose configuration, using [buildrun/docker/docker-compose/dev-env/docker-compose.yml](buildrun/docker/docker-compose/dev-env/docker-compose.yml)
service `web` and name it `quiz_app-web DEV`
The `quiz_app` run configuration should work as is after that


## Network configuration
Ports [80, 443, 5432] must be available on your machine.

### DNS
On a Unix machine, add the following rule to `/etc/hosts`:
```
127.0.0.1	local-quizapp.domain.ovh
```

### Certificate
To be able to correctly run your website in HTTPS without your browser protesting about an invalid
certificate, you'll need to manually add and trust the Caddy root certificate located [here](buildrun/docker/caddy/.caddy/data/caddy/pki/authorities/local/root.crt)
On a Mac, simply open this file using Keychain Access, then double-click on the certificate called "Caddy Local Authority"
once it has been added to System keychain, and in the Trust settings select "Always Trust".
If your browser still display the certificate as invalid after that, restart your browser.

### Urls
Don't use `localhost` as you'll have errors with the HTTPS configuration.
- quiz_app website: https://local-quizapp.domain.ovh/ (if you get a warning about invalid certificate, see previous section)
- quiz_app openAPI interface: https://local-quizapp.domain.ovh/api/v1/schema/swagger-ui/


# Quiz application's gotcha

- If you get CORS error when trying to call this backend from a SPA, check that the domain name used to run your SPA
  is put inside [`CORS_ALLOWED_ORIGINS`](buildrun/docker/quiz_app/dev.env) (restart the backend if you changed this setting, the chosen default is standard for angular app run locally)
  and that you get no certificate error when trying to [access the app from your browser](https://local-quizapp.domain.ovh/api/v1/schema/swagger-ui/)
- The questions are automatically ordered by insertion date, using the [`order_with_respect_to` django's mechanism](https://docs.djangoproject.com/en/4.0/ref/models/options/#order-with-respect-to)

# How to add a new Python package requirement

Add you requirement to buildrun/docker/quiz_app/requirements/base-requirements.in
(or dev-* / prod-* / test-* if your package is only useful in one context).
Then run:
```shell
cd buildrun/docker/docker-compose/dev-env
task compile-dep
# Don't forget to rebuild the service to include the new dependency
docker-compose up -d --no-recreate --build web
```
**/!\ The compile-dep service also do an upgrade of all package,
remove the `--upgrade` option in the docker-compose file from all the commands called to avoid that**
