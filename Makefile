.PHONY: clean black isort prettify pretty debug release run run-release

clean:
	rm -rf ./build
	rm -rf ./dist

debug:
	pyoxidizer build

# release:
# 	python ./version.py --write
# 	pyoxidizer build --release

run:
	@./build/x86_64-unknown-linux-gnu/debug/install/pfd
