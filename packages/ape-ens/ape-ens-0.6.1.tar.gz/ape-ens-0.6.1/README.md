# Quick Start

Ape plugin for ENS argument conversion and contracts

## Dependencies

- [python3](https://www.python.org/downloads) version 3.8 up to 3.11.

## Installation

### via `pip`

You can install the latest release via [`pip`](https://pypi.org/project/pip/):

```bash
pip install ape-ens
```

### via `setuptools`

You can clone the repository and use [`setuptools`](https://github.com/pypa/setuptools) for the most up-to-date version:

```bash
git clone https://github.com/ApeWorX/ape-ens.git
cd ape-ens
python3 setup.py install
```

## Quick Usage

The ENS plugin requires a mainnet connection to resolve ENS names because ENS contracts are only deployed to mainnet.
Thus, the first thing you should do is ensure you have configured a mainnet provider.
For example, if you use `infura` or `alchemy`, install the associated plugin:

```bash
ape plugins install infura
```

Afterwards, you should see it in the output of the `list` command:

```bash
$ ape plugins list

Installed Plugins:
  infura      0.4.0
  ...
```

After your provider plugin of choice is installed, configure it to be your default mainnet provider in your `ape-config.yaml` file:

```yaml
ethereum:
  mainnet:
    default_provider: infura
```

Finally, you can start the ape console using any network of your choice:

```bash
ape console --network :rinkeby:infura
```

Then, convert an `ens` domain to an `AddressType`:

```python
In [1]: from ape.types import AddressType
In [2]: convert("vitalik.eth", AddressType)
Out[2]: '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045'
```

The ENS plugin temporarily connects to mainnet, caches the address resolution, and then your original network uses the result.
