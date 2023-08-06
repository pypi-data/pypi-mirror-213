all: net-genconfig

remake: clean all

net-genconfig:
	./setup.py sdist bdist_wheel

upload:
	python3 -m twine upload dist/*

clean:
	rm -rf build dist net_genconfig.egg-info
