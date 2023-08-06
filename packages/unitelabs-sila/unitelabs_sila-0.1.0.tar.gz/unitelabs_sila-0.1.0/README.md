![pipeline](https://gitlab.com/unitelabs/integrations/sila2/sila-python/badges/main/pipeline.svg?ignore_skipped=true)
![coverage](https://gitlab.com/unitelabs/integrations/sila2/sila-python/badges/main/coverage.svg?job=test)
![release](https://gitlab.com/unitelabs/integrations/sila2/sila-python/badges/release.svg)
![license](https://img.shields.io/gitlab/license/unitelabs/integrations/sila2/sila-python)

# SiLA

This repository is an un-opinionated library that provides you with all means to develop a SiLA 2 1.1 compliant python
application. It adheres to the [SiLA 2 specification](https://sila2.gitlab.io/sila_base/) and is used by the [UniteLabs 
Connector Framework](https://gitlab.com/unitelabs/connector-framework/) to enable rapid development of cloud-native SiLA 
Servers with a code-first approach.

## Installation

The SiLA library requires Python 3.9 or later. To get started quickly, we recommend to use the [UniteLabs Connector
Framework](https://gitlab.com/unitelabs/connector-framework/) to develop your SiLA 2 server. Clone one of the starter
projects with:

```
$ git clone https://gitlab.com/unitelabs/connector-starter.git my-connector
$ cd my-connector
$ poetry install
$ poetry run connector start
```

You can also manually create a new project from scratch and install the library with pip. In this case, of course,
you'll be responsible for creating the project boilerplate files yourself.

```
pip install unitelabs-sila
```

## Documentation

🧱🚧🏗️ This is still work in progress 🧱🚧🏗️  

## Contribute

Submit and share your work!
https://hub.unitelabs.ch

Please submit your feature requests and bug reports using the GitLab issue system with a clear description.
If you have further questions, issues, or suggestions for improvement, don't hesitate to reach out to us at
[developers@unitelabs.ch](mailto:developers+sila@unitelabs.ch).

Join the Python channel in the [SiLA Slack](https://sila-standard.org/slack)
workspace to stay up-to-date with new developments and announcements from the community.

## License

This code is licensed under the [MIT license](LICENSE).
