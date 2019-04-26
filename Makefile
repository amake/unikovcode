SHELL := /bin/bash -O extglob
UNICODE_DATA := vendor/UnicodeData.txt
PAYLOAD := dist/lambda-deploy.zip
LAMBDA_NAME := UnikovcodeTwitterBot
AWS_ARGS ?=

.PHONY: zip
zip: $(PAYLOAD)

.env:
	virtualenv .env
	.env/bin/pip install -e .

dist vendor:
	mkdir -p $(@)

.PHONY: clean
clean:
	rm -rf dist

.PHONY: cleanAll
cleanAll:
	rm -rf dist vendor

.PHONY: update
update: | .env
	.env/bin/pip install --upgrade -e .
	rm -rf vendor
	$(MAKE) $(UNICODE_DATA)

$(PAYLOAD): *.py credentials.json $(UNICODE_DATA) | .env dist
	rm -rf $(@)
	zip $(@) $(^) -x \*.pyc
	cd .env/lib/python3.6/site-packages; \
		zip -r $(PWD)/$(@) ./!(pip*|wheel*|setuptools*|easy_install*) -x \*.pyc

credentials.json:
	.env/bin/python auth_setup.py

$(UNICODE_DATA): | vendor
	curl -o $(@) http://unicode.org/Public/UNIDATA/$(@F)

.PHONY: deploy
deploy: $(PAYLOAD)
	aws $(AWS_ARGS) lambda update-function-code \
		--function-name $(LAMBDA_NAME) \
		--zip-file fileb://$$(pwd)/$(<)

.PHONY: invoke
invoke:
	aws $(AWS_ARGS) lambda invoke \
		--function-name $(LAMBDA_NAME) \
		/dev/null

.PHONY: test
test: | .env $(UNICODE_DATA)
	.env/bin/python unikovcode.py