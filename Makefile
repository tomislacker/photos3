AWS_PROFILE  := personal
REGION       := us-east-1
PWD          := $(shell pwd)
PYVER        := 3.6
VENV_PATH    := venv

BUILDER_IMAGE_TAG := photos3/python-builder


.PHONY : stack
stack  :
	AWS_PROFILE=$(AWS_PROFILE) \
	ansible-playbook \
		-i regions \
		-l $(REGION) \
		stack.yml \
		-e s3_deploy_key=$(shell make build.zip.sha256) \
		--diff \
		-vvv

.PHONY : util
util   :
	make -C util all

.PHONY    : build.zip
build.zip :
	docker run \
		-it \
		--rm \
		-v $(PWD):/code \
		-w /code \
		-e BUILD_ZIP=$@ \
		$(BUILDER_IMAGE_TAG)
	zip -ur $@ photos3 -x "*.pyc"

.PHONY           : build.zip.sha256
build.zip.sha256 :
	@sha256sum build.zip \
		| cut -d' ' -f1

.PHONY       : deploy-build
deploy-build :
	AWS_PROFILE=$(AWS_PROFILE) \
		aws s3 cp \
			build.zip \
			s3://$(shell AWS_PROFILE=$(AWS_PROFILE) aws cloudformation describe-stacks --stack-name photos3 | jq -r '.Stacks[0].Outputs | .[] | select(.OutputKey=="UploadBucket") | .OutputValue')/code/$(shell make build.zip.sha256).zip

venv :
	virtualenv -p python$(PYVER) $(VENV_PATH)

.PHONY  : version
version : venv
	@echo "from photos3 import __version__; print(__version__)" | $(VENV_PATH)/bin/python
