AWS_PROFILE  := personal
REGION       := us-east-1


.PHONY : stack
stack  :
	AWS_PROFILE=$(AWS_PROFILE) \
	ansible-playbook \
		-i regions \
		-l $(REGION) \
		stack.yml \
		--diff \
		-vvv
