pushd prepare
	./run.sh || exit 1
popd
./cleanup.sh || exit
./compile.sh || exit
./upload.sh || exit
echo "produce workflow finished"