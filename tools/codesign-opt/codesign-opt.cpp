#include "codesign/Passes.h"
#include "mlir/Dialect/Func/IR/FuncOps.h"
#include "mlir/Dialect/Arith/IR/Arith.h"
#include "mlir/Dialect/Affine/IR/AffineOps.h"
#include "mlir/Dialect/SCF/IR/SCF.h"
#include "mlir/Dialect/MemRef/IR/MemRef.h"
#include "mlir/IR/Dialect.h"
#include "mlir/IR/MLIRContext.h"
#include "mlir/Pass/Pass.h"
#include "mlir/Pass/PassManager.h"
#include "mlir/Tools/mlir-opt/MlirOptMain.h"
#include "llvm/Support/CommandLine.h"
#include "llvm/Support/InitLLVM.h"

#include "mlir/Dialect/Linalg/IR/Linalg.h"
#include "mlir/Dialect/ControlFlow/IR/ControlFlow.h"
#include "mlir/Dialect/Math/IR/Math.h"
#include "mlir/Dialect/Complex/IR/Complex.h"
#include "mlir/Dialect/UB/IR/UBOps.h"
#include "mlir/Dialect/MLProgram/IR/MLProgram.h"
#include "mlir/Dialect/Tensor/IR/Tensor.h"


int main(int argc, char **argv) {
  mlir::DialectRegistry registry;
  
  // Register dialects manually (no registerAllDialects function)
  registry.insert<mlir::func::FuncDialect,
                  mlir::arith::ArithDialect,
                  mlir::affine::AffineDialect,
                  mlir::scf::SCFDialect,
                  mlir::tensor::TensorDialect,
                  mlir::memref::MemRefDialect,
                  mlir::linalg::LinalgDialect,
                  mlir::cf::ControlFlowDialect,
                  mlir::math::MathDialect,
                  mlir::complex::ComplexDialect,
                  mlir::ub::UBDialect,
                  mlir::ml_program::MLProgramDialect>();
  
  // Register your custom passes
  // registerCodeSignPasses();
  codesign::registerCodeSignPasses();
  
  return mlir::asMainReturnCode(
      mlir::MlirOptMain(argc, argv, "CodeSign optimizer driver\n", registry));
}