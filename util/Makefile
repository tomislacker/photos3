BUILDER_IMAGE_TAG := photos3/python-builder


.PHONY       : python-image
all          : python-image
python-image :
	docker build \
		-t $(BUILDER_IMAGE_TAG) \
		.
