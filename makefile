SHELL := /bin/bash -O extglob
unicode-data := vendor/UnicodeData.txt
payload := dist/lambda-deploy.zip
lambda-name := UnikovcodeTwitterBot

.PHONY = zip clean cleanAll update deploy test

zip: $(payload)

.env:
	virtualenv .env
	.env/bin/pip install -e .

dist vendor:
	mkdir -p $(@)

clean:
	rm -rf dist

cleanAll:
	rm -rf dist vendor

update: | .env
	.env/bin/pip install --upgrade -e .
	rm -rf vendor
	$(MAKE) $(unicode-data)

$(payload): *.py credentials.json $(unicode-data) | .env dist
	rm -rf $(@)
	zip $(@) $(^) -x \*.pyc
	root=$$(pwd); cd .env/lib/python3.6/site-packages; \
		zip -r $$root/$(@) ./!(pip*|wheel*|setuptools*|easy_install*) -x \*.pyc

credentials.json:
	.env/bin/python auth_setup.py

$(unicode-data): | vendor
	curl -o $(@) http://unicode.org/Public/UNIDATA/$(@F)

deploy: $(payload)
	aws lambda update-function-code \
		--function-name $(lambda-name) \
		--zip-file fileb://$$(pwd)/$(<)

test: | .env $(unicode-data)
	.env/bin/python unikovcode.py
