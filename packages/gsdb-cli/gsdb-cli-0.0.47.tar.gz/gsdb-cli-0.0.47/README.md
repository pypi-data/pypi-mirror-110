# GeoSpock DB CLI

## Installing the CLI from pip
```
    $ python -m pip install gsdb-cli
```

### Logging in with your enterprise Identity Provider
The `configure` command creates a configuration file with the endpoint for your deployment and saves your username 
and password to your computer's secure keychain.

Alternatively, if you do not want to save your details: 
 - all commands can be run with `gsdb --user <value> --password <value> --endpoint <value> COMMAND`.
 - the CLI will also check for the environment variables `GEOSPOCK_USER` and `GEOSPOCK_PASSWORD` and use these to 
 authenticate. An environment variable `GEOSPOCK_ENDPOINT` can also be used to provide the request address.

An optional `--profile <value>` argument can be used to set up configurations for multiple GeoSpock DB deployments.
All subsequent `gsdb` commands can then use this profile flag to specify that deployment, e.g. 
`gsdb --profile dev COMMAND`.

## Running the CLI
The CLI can be activated at the command line using `gsdb [--profile <value>] COMMAND ... `

A list of commands can be shown by using `gsdb --help`. Further information on the input types of each command can be 
obtained by running `gsdb COMMAND --help`.

