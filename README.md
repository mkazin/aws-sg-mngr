# aws-sg-mngr - AWS SecurityGroup Manager

[![Build Status](https://travis-ci.org/mkazin/aws-sg-mngr.svg?branch=master)](https://travis-ci.org/mkazin/aws-sg-mngr)
[![Code Climate](https://codeclimate.com/github/mkazin/aws-sg-mngr/badges/gpa.svg)](https://codeclimate.com/github/mkazin/aws-sg-mngr)
[![Test Coverage](https://codeclimate.com/github/mkazin/aws-sg-mngr/badges/coverage.svg)](https://codeclimate.com/github/mkazin/aws-sg-mngr/coverage)

A somewhat-more sane interface to AWS Security Groups.

What does that mean?

Basically, the goal is to provide a human-centric API, rather than assume a DevOps guru
is managing security groups using a custom-built configuration-as-code system.

## Goals 
Among other things, it aims to:
- Treat SG like a list of firewall rules (the only nesting is [SG] contains [Rules])
- Get rid of AWS' excessive nesting (e.g. a nested "IpRanges" list within "IpPermissionsEgress")
- Instead, allow simple REST requests with QueryParams rather than a complicated Body
- Provide name resolution for CIDRs and SG IDs because "72.55.31.24/32" or "sg-1234asdf" aren't memorable
- Allow easy IP switches (e.g. for use in DHCP IP lease expiration for home users)
- Possibly also include CIDR expansion (e.g. when registering a subnet rather than an IP)
- Implement a rule expiration system (e.g. for use when working on the road, from a cafe)
- Allow for extending the list of named ports, configurable by the admin

### Scope
A quick note on project scope.

This project is intended to provide an API, as a replacement for AWS' API.

Things that are not expected to be included here:
- Clients! There are no plans to include web, mobile, or integrations (Slack, IFTTT, etc.) in this project. Those belong in separate GitHub projects, hopefully led by other maintainers who will do them justice. 
- Servers! Due to security needs (i.e. your AWS secret keys) a server of some sort will need to be deployed by users. That's entirely on you, with one minor exception- I will be providing the basic server implementation I will be using myself. It may not satisfy your needs, and will not be the focus of this project, but rather it will provide a reference implementation.

That being said,
- If you create a client, I will certainly link to your project.
- If you implement a server based on this project, get in touch and we'll discuss the best way to help share that. I expect to include a list of articles demonstrating various implementations. This repository may consider including code snippets (e.g. an AWS Lambda/API-Gateway-based backend) and example config files (e.g. Nginx proxy).


## Contributing

I'm still just getting this project off the ground (I'm trying to do it "the right way" by releasing it before it's "ready", so please bear with me).

Feel free to work on anything with the label "help wanted". Get in touch if you want to take something off my plate, make a suggestion, ask a question, chat, etc.
