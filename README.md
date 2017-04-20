# Route 53 Lane Change

This is a tool to update your dynamic IP address in AWS Route 53

## Pre-requisites for running

Docker installed

## Testing

Run make test to build a docker container and run unit tests

## Building

Run ```make docker``` to generate a docker container called dns-updater

## Running

### Environment Variables

ROOT - The zone to update records in. eg example.com
SUBDOMAINS - The record names that will be updated in the zone, this can be a comma seperated list. eg subdomain or subdomain1,subdomain2 ( This will example to subdomain.example.com)
CHECK_INTERVAL - The interval to check that dns is correct default 60

### Boto config

You will need to provide boto configuration for the AWS connection
Options for this can be found on http://boto.cloudhackers.com/en/latest/boto_config_tut.html

The main 2 options are to pass in environment variables or inject a file into the container


### Starting the container 

docker run -t -i -e ROOT=<your domain> -e SUBDOMAINS=subdomain dns-updater


