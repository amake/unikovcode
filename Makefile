SHELL := /bin/bash -O extglob
VENV := .env
PYTHON_VERSION := 3.9
UNICODE_VERSION := 14.0.0
UNICODE_DATA := vendor/UnicodeData.txt
PAYLOAD := dist/lambda-deploy.zip
LAMBDA_NAME := UnikovcodeTwitterBot
AWS_ARGS ?=

.PHONY: zip
zip: $(PAYLOAD)

$(VENV):
	virtualenv --python $(PYTHON_VERSION) $(@)
	$(@)/bin/pip install -e .

dist vendor:
	mkdir -p $(@)

.PHONY: clean
clean: ## Remove generated data
clean:
	rm -rf dist

.PHONY: update
update: ## Update dependencies and vendor data
update: | $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install --upgrade --upgrade-strategy eager -e .
	rm -rf vendor
	$(MAKE) assets

$(PAYLOAD): *.py credentials.json $(UNICODE_DATA) | $(VENV) dist
	rm -rf $(@)
	zip $(@) $(^) -x \*.pyc
	cd $(VENV)/lib/python$(PYTHON_VERSION)/site-packages; \
		zip -r $(PWD)/$(@) ./!(pip*|wheel*|setuptools*|easy_install*) -x \*.pyc

credentials.json:
	$(VENV)/bin/python auth_setup.py

.PHONY: assets
assets: ## Prepare assets
assets: $(UNICODE_DATA)

$(UNICODE_DATA): | vendor
	curl -o $(@) https://unicode.org/Public/$(UNICODE_VERSION)/ucd/$(@F)

.PHONY: deploy
deploy: ## Deploy lambda payload to AWS
deploy: $(PAYLOAD)
	aws $(AWS_ARGS) lambda update-function-code \
		--function-name $(LAMBDA_NAME) \
		--zip-file fileb://$$(pwd)/$(<)

.PHONY: invoke
invoke: ## Invoke lambda on AWS
invoke:
	aws $(AWS_ARGS) lambda invoke \
		--function-name $(LAMBDA_NAME) \
		/dev/null

.PHONY: test
test: ## Run local test
test: | $(VENV) $(UNICODE_DATA)
	$(VENV)/bin/python unikovcode.py

.PHONY: help
help: ## Show this help text
	$(info usage: make [target])
	$(info )
	$(info Available targets:)
	@awk -F ':.*?## *' '/^[^\t].+?:.*?##/ \
         {printf "  %-24s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
