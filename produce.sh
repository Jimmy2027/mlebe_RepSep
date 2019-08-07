pushd prepare
	./run.sh || exit
popd
./cleanup.sh || exit
./compile.sh || exit
./upload.sh || exit
