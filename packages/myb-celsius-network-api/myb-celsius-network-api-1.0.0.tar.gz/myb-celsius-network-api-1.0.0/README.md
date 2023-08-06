# myb-celsius-network-api
 An API client for the Celsius Network (Wallet) API

## Installation

The package is availble via PyPi and can be installed with the following command:
```
pip3 install myb-celsius-network-api
```

To install it from the repo, clone the repo and cd into the directory:

```
git clone https://github.com/mine-your-business/myb-celsius-network-api.git
cd myb-celsius-network-api
```

You can install this library with `pip`:

```
pip3 install .
```

## Testing

Celsius Network offers a number of different "partner" integrations. The one this library leverages is the "Omnibus Treasury" partnership which is documented [here][omnibus-treasury].

Instructions on how to acquire a partner token are described in that document and it links to a guide on [generating an API key][api-key].

Postman Docs for their API can be found [here][omnibus-postman-docs].

Before tests can be run, a `local_env_vars.py` file needs to be created in the [`tests`](tests) folder. You can use the [`local_env_vars_example.py`](tests/local_env_vars_example.py) file as an example for the content - just be sure to fill out the API key and token data with actual secrets from Celsius Network.

To run tests, simply run the following command:

```
pytest --verbose
```

To print output of tests, run the following:
```
pytest --verbose -s
```

## Releases

Releases should follow a [Semantic Versioning][semver] scheme. 

When changes have been made that warrant a new release that should be published, modify the `__version__` in [`setup.py`](setup.py) 

After the change is merged to the `main` branch, go to [releases][releases] and `Draft a new release`. The `Tag version` should follow the pattern `v1.0.0` and should `Target` the `main` branch. 

The `Release title` should not include the `v` from the tag and should have a reasonably detailed description of the new release's changes. 

Once the release has been published, the [`.github/workflows/python-publish.yml`][publish] GitHub Actions Workflow should trigger and automatically upload the new version to [PyPi]][pypi] using GitHub secrets credentials stored with the [Mine Your Business GitHub Organization][myb].


[api-key]: https://developers.celsius.network/createAPIKey.html
[myb]: https://github.com/mine-your-business
[omnibus-treasury]: https://developers.celsius.network/omnibus-treasury.html
[omnibus-postman-docs]: https://documenter.getpostman.com/view/4207695/Rzn6v2mZ#83677182-2cc9-4198-b574-77ad0862237b
[publish]: .github/workflows/python-publish.yml
[pypi]: https://pypi.org/
[releases]: https://github.com/mine-your-business/myb-celsius-network-api/releases
[semver]: https://semver.org/
