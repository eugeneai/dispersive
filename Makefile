.PHONY: all test xray rake edit activate

all: test

test: xray

xray:
	./icc_xray_app.sh

rake:
	./icc_rake_app.sh

edit:
	scite &

activate:
	. ./python/bin/activate
