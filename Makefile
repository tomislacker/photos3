AWS_PROFILE  := personal
REGION       := us-east-1
PWD          := $(shell pwd)

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
