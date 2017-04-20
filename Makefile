test: docker
	docker build -t dns-updater-test -f Dockerfile.test . 	
	docker run --rm -t -i dns-updater-test

docker:
	docker build -t dns-updater .
