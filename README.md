
# rchain-keys-generator

Python helper to generate new private/public keys pair to run RChain node as validator

## what this package does

Current implemented workflow is:
1. run RNode in standalone mode for one validator with a temporary data folder
2. a thread interrupt the node process running when keys have been generated
3. copy and parse the `.sk` key file from data folder
4. remove temporary data folder


## prerequisites

- rnode package installed
- rnode binary in `PATH`
- python3.5+ installed (together with pip package system)


## todo

- [x] working first version based only on standard library
- [x] parameter to output to file to be sourced
- [x] setup as package
- [ ] publish manually on pypi
- [ ] unittests
- [ ] travis ci
- [ ] automatic pypi publishing from tags
