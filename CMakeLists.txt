cmake_minimum_required(VERSION 3.20)
project(CodeSignOpt LANGUAGES C CXX)

# Point to the *build* of the llvm submodule.
set(LLVM_DIR "${CMAKE_SOURCE_DIR}/llvm-build/lib/cmake/llvm")
set(MLIR_DIR "${CMAKE_SOURCE_DIR}/llvm-build/lib/cmake/mlir")

find_package(LLVM REQUIRED CONFIG)
find_package(MLIR REQUIRED CONFIG)

message(STATUS "Found LLVM at: ${LLVM_DIR}")
message(STATUS "Found MLIR at: ${MLIR_DIR}")

list(APPEND CMAKE_MODULE_PATH "${LLVM_CMAKE_DIR}")
list(APPEND CMAKE_MODULE_PATH "${MLIR_CMAKE_DIR}")

include(AddLLVM)
include(AddMLIR)
include(HandleLLVMOptions)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED YES)

include_directories(
  ${LLVM_INCLUDE_DIRS}
  ${MLIR_INCLUDE_DIRS}
  ${CMAKE_CURRENT_SOURCE_DIR}/include
)

add_definitions(${LLVM_DEFINITIONS})

add_subdirectory(lib)
add_subdirectory(tools/codesign-opt)
