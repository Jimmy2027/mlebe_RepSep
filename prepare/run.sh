#!/usr/bin/env bash

for i in *py; do
	python $i || exit 1
done
