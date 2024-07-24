# Reset
COLOR_OFF="\033[0m"

# Regular Colors
BLACK="\033[0;30m"
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
BLUE="\033[0;34m"
PURPLE="\033[0;35m"
CYAN="\033[0;36m"
WHITE="\033[0;37m"

GIT_TAG ?= latest

login_ecr:
	aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 567925872059.dkr.ecr.ap-northeast-2.amazonaws.com

handle_image:
	docker buildx build \
	${BUILD_IMAGE_OPTION} \
	--platform linux/amd64 \
	-t ${REGISTRY_PREFIX_TESTER}/tester:${GIT_TAG} \
	-f ./Dockerfile .

# Need GIT_TAG
build_image: BUILD_IMAGE_OPTION=--load
build_image: handle_image

# Need GIT_TAG
push_image: BUILD_IMAGE_OPTION=--push
push_image: handle_image

.PHONY: all
all:
.PHONY: clean
clean:
.PHONY: test
test:
