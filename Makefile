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
		--diff \
		-vvv

.PHONY    : build.zip
build.zip :
	docker run \
		-it \
		--rm \
		-v $(PWD):/code \
		-w /code \
		$(BUILDER_IMAGE_TAG)

venv :
	virtualenv -p python$(PYVER) $(VENV_PATH)

.PHONY  : version
version : venv
	@echo "from photos3 import __version__; print(__version__)" | $(VENV_PATH)/bin/python
