#!/bin/bash

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

export VIRTUAL_ENV_DISABLE_PROMPT=1
source venv/bin/activate

export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
export LOG_LEVEL=debug

export PS1="(faasm) $PS1"

export FAASM_ROOT=$(pwd)
export FAASM_VERSION=$(cat VERSION)
export FAASM_CMAKE_TOOLCHAIN=$FAASM_ROOT/toolchain/FaasmToolchain.cmake
export FAASM_BASH_TOOLCHAIN=$FAASM_ROOT/toolchain/env.sh

alias fm="inv"
