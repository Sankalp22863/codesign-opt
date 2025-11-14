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

int main(int argc, char **argv) {
  mlir::DialectRegistry registry;
  
  // Register dialects manually (no registerAllDialects function)
  registry.insert<mlir::func::FuncDialect,
                  mlir::arith::ArithDialect,
                  mlir::affine::AffineDialect,
                  mlir::scf::SCFDialect,
                  mlir::memref::MemRefDialect>();
  
  // Register your custom passes
  // registerCodeSignPasses();
  codesign::registerCodeSignPasses();
  
  return mlir::asMainReturnCode(
      mlir::MlirOptMain(argc, argv, "CodeSign optimizer driver\n", registry));
}