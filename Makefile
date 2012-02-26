.PHONY: all test xray rake edit

all: test

test: xray

xray:
	./icc_xray_app.sh

rake:
	./icc_rake_app.sh

edit:
	scite &
