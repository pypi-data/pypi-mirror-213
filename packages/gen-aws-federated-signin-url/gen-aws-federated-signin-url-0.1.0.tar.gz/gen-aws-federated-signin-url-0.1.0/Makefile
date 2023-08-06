.DEFAULT_GOAL := help


## build
build:
	python -m build

## clean
clean:
	rm -rf dist/ build/ src/*.egg-info src/gen_aws_federated_signin_url/_version.py

## help
help:
	@make2help $(MAKEFILE_LIST)


.PHONY: help
.SILENT:
