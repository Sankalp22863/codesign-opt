#!/usr/bin/env bash

set -euo pipefail

### CONFIG #####################################################################

# Directory layout (relative to this script / repo root)
ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LLVM_SRC_DIR="${ROOT_DIR}/llvm-project"
LLVM_BUILD_DIR="${ROOT_DIR}/llvm-build"
TOOL_BUILD_DIR="${ROOT_DIR}/build"

# Number of parallel jobs
if command -v nproc &>/dev/null; then
  JOBS="$(nproc)"
elif [[ "$(uname)" == "Darwin" ]]; then
  JOBS="$(sysctl -n hw.ncpu)"
else
  JOBS=4
fi

###############################################################################
echo ">>> Root dir: ${ROOT_DIR}"
echo ">>> LLVM source dir (submodule): ${LLVM_SRC_DIR}"
echo ">>> LLVM build dir:              ${LLVM_BUILD_DIR}"
echo ">>> Tool build dir:              ${TOOL_BUILD_DIR}"
echo ">>> Using ${JOBS} parallel jobs"
echo

###############################################################################
### 1. Update llvm-project submodule
###############################################################################
echo ">>> Syncing llvm-project submodule URL from .gitmodules ..."
git -C "${ROOT_DIR}" submodule sync -- llvm-project

echo ">>> Initializing / updating llvm-project submodule ..."
git -C "${ROOT_DIR}" submodule update --init --recursive llvm-project

if [[ ! -d "${LLVM_SRC_DIR}" ]]; then
  echo "ERROR: llvm-project submodule directory not found at ${LLVM_SRC_DIR}"
  echo "Make sure the llvm-project submodule is correctly configured."
  exit 1
fi

echo ">>> llvm-project submodule is ready at ${LLVM_SRC_DIR}"
echo

###############################################################################
### 2. Configure + build LLVM/MLIR
###############################################################################
echo ">>> Configuring LLVM+MLIR in ${LLVM_BUILD_DIR} ..."

mkdir -p "${LLVM_BUILD_DIR}"

# Use Ninja if available, otherwise default generator
GENERATOR="Unix Makefiles"
if command -v ninja &>/dev/null; then
  GENERATOR="Ninja"
fi

cmake -S "${LLVM_SRC_DIR}/llvm" \
      -B "${LLVM_BUILD_DIR}" \
      -G "${GENERATOR}" \
      -DLLVM_ENABLE_PROJECTS="mlir" \
      -DLLVM_TARGETS_TO_BUILD="host" \
      -DCMAKE_BUILD_TYPE=Release

echo ">>> Building LLVM+MLIR ..."
if [[ "${GENERATOR}" == "Ninja" ]]; then
  ninja -C "${LLVM_BUILD_DIR}" -j "${JOBS}"
else
  cmake --build "${LLVM_BUILD_DIR}" -- -j "${JOBS}"
fi

echo

###############################################################################
### 3. Configure + build codesign-opt tool
###############################################################################
echo ">>> Configuring codesign-opt in ${TOOL_BUILD_DIR} ..."

mkdir -p "${TOOL_BUILD_DIR}"

cmake -S "${ROOT_DIR}" \
      -B "${TOOL_BUILD_DIR}" \
      -G "${GENERATOR}" \
      -DLLVM_DIR="${LLVM_BUILD_DIR}/lib/cmake/llvm" \
      -DMLIR_DIR="${LLVM_BUILD_DIR}/lib/cmake/mlir"

echo ">>> Building codesign-opt ..."
if [[ "${GENERATOR}" == "Ninja" ]]; then
  ninja -C "${TOOL_BUILD_DIR}" codesign-opt -j "${JOBS}"
else
  cmake --build "${TOOL_BUILD_DIR}" --target codesign-opt -- -j "${JOBS}"
fi

echo
echo "======================================================================="
echo " Build completed successfully."
echo
echo " LLVM built at:   ${LLVM_BUILD_DIR}"
echo " Tool built at:   ${TOOL_BUILD_DIR}/tools/codesign-opt/codesign-opt"
echo
echo " Example usage:"
echo "   ${TOOL_BUILD_DIR}/tools/codesign-opt/codesign-opt \\"
echo "       path/to/input.mlir -lower-maximumf > out.mlir"
echo "======================================================================="
