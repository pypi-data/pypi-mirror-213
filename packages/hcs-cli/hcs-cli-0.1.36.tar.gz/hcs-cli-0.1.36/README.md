# horizon-cloud-service-cli

## Overview
Command line toolbox for [VMware Horizon Cloud Service (HCS) Next-Gen](https://www.vmware.com/products/horizon-cloud.html). It provides human-friendly operations based on HCS REST API.

## Try it out


### Prerequisites
* Python 3.10+
* Pip3

Refer to [Setup Prerequisites](doc/dev-setup.md#setup-prerequisites) for more details.

### Use the published version on PyPI

#### Mac & Linux

Install the tool
```
pip3 install hcs-cli
```
Initialize a profile with interactively, with credential. 
```
hcs profile init
```

To get a valid token to use with the CLI, refer to doc [Get CSP User API Token](doc/get-csp-user-api-token.md).


Run a command, for example, list templates:
```
hcs admin template list
```

## Documentation

* [HCS CLI Cheatsheet](doc/hcs-cli-cheatsheet.md)

* [Development Setup](doc/dev-setup.md)

* Based on [Context Programming](https://github.com/nanw1103/context-programming)

  
## Contributing

The horizon-cloud-service-cli project team welcomes contributions from the community. Before you start working with horizon-cloud-service-cli, please read and sign our [Contributor License Agreement CLA](CONTRIBUTING_CLA.md). If you wish to contribute code and you have not signed our contributor license agreement (CLA), our bot will prompt you to do so when you open a Pull Request. For any questions about the CLA process, please refer to our [FAQ]([https://cla.vmware.com/faq](https://cla.vmware.com/faq)).

## License

Apache 2.0


