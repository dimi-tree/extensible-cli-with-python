# Contributing to kbk CLI 

## Development
This project uses Poetry for dependency management and packaging.

To install dependencies for development, run: 
```
poetry install 
```

To run locally:
```
poetry run kbk help
```

## Testing
Use Make to run tests

For unit tests:

```
make test
```

Integration test:
```
make integration
```

Behave Integration tests are implemented by invoking the CLI through the package installed in the Poetry virtual
 environment. 
 
Individual tests can be run by Feature:

`behave -i cli.feature`

Or individual scenarios:

`behave -n 'Document Available Commands'`


## Publishing
*NOTE:* This project is currently publishing to TestPyPI repository because the project is for educational purposes. 

Update the `version` in `pyproject.toml`.

To publish a build to PyPI the commit needs to be tagged

```
git tag -a v1.2
git push --tags
```

## Contributing

1. Create your feature branch (`git checkout -b feature/fooBar`)
1. Commit your changes (`git commit -am 'Add some fooBar'`)
   - NOTE: this project uses git pre-commit hooks to format and lint code changes to align with standard conventions. 
1. Push to the branch (`git push origin feature/fooBar`)
1. Create a new Pull Request


## Release History

* 0.0.x
    * Proof of Concept
