
UIS=main_win.py spectra.py

all: $(UIS)

.PHONY:	all

%.py: %.ui
	pyuic4 -o $@ $<
