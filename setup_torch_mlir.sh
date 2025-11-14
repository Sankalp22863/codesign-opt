cmake -S llvm-project/llvm -B llvm-build -G Ninja \
  -DLLVM_ENABLE_PROJECTS="mlir" \
  -DMLIR_ENABLE_BINDINGS_PYTHON=ON \
  -DPython3_EXECUTABLE="$(which python3)" \
  -DCMAKE_BUILD_TYPE=Release


# Updating the LLVM to the 18.0.10 release.


rm -rf llvm-build
mkdir llvm-build

cmake -S llvm-project/llvm -B llvm-build -G Ninja \
  -DLLVM_ENABLE_PROJECTS="mlir" \
  -DCMAKE_BUILD_TYPE=Release

cmake --build llvm-build --target mlir-opt -j8


cmake -S . -B build \
  -DLLVM_DIR=llvm-build/lib/cmake/llvm \
  -DMLIR_DIR=llvm-build/lib/cmake/mlir


  cmake --build build --target codesign-opt -j8

# Stable working LLVM 18.1.8.



