
# rchain-keys-generator

Python helper to generate new private/public keys pair to run RChain node as validator


## implementation

Current implemented workflow:

1. run RNode in standalone mode for one validator with a temporary data folder
2. a thread interrupt the node process running when keys have been generated
3. copy and parse the `.sk` key file from data folder
4. remove temporary data folder


## quick start

Here's a brief overview on how to use the package

### prerequisites

- rnode package installed (see [official instructions](https://rchain.atlassian.net/wiki/spaces/CORE/pages/428376065/User+guide+for+running+RNode#UserguideforrunningRNode-InstallingRNode))
- rnode binary in `PATH`
- python3.5+ installed (together with pip package system)

### install

Installation is done via the official Python package manager:
```bash
pip3 install rchain-keygen
```

### generate keys

After installing you will be able to use the binary as:
```bash
$ rchain-keygen --help
usage: rchain-keygen [-h] [--save-as-source]

RChain 'ed25519' signed keys generator

optional arguments:
  -h, --help        show this help message and exit
  --save-as-source  enable saving variables for bash env sourcing
```

Having `rnode` installed you just need to run:
```bash
rchain-keygen

[...]
Launching: rnode.
[...]

VALIDATOR_PUBLIC_KEY=...
VALIDATOR_PRIVATE_KEY=...

```

### use inside official RChain node docker images

That would be as easy as:
```bash
docker run --rm -it --entrypoint /bin/bash rchain/rnode:release-rnode-v0.7
# container shell
export PATH=/opt/docker/bin:$PATH
apt update && apt install -y python3-pip
pip3 install rchain-keygen
cd $HOME
rchain-keygen
```


### troubleshooting

1. missing `rnode` installation (or not being found in PATH) would end up execution with Exception:

```bash
$ rchain-keygen
Temporary dir: ...
Launching: rnode.

[...]
FileNotFoundError: [Errno 2] No such file or directory: 'rnode'
```


## development

Black formatter:
```bash
docker run --rm -it \
    -v (pwd):/code -w /code \
    unibeautify/black -S ./rchain_keygen
```


## todo

- [x] working first version based only on standard library
- [x] parameter to output to file to be sourced
- [x] setup as package
- [x] formatter
- [x] docs
- [ ] publish manually on pypi + first tag
- [ ] unittests
- [ ] travis ci
- [ ] automatic pypi publishing from tags
