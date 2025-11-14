#include "codesign/Passes.h"

#include "mlir/Dialect/Arith/IR/Arith.h"
#include "mlir/Dialect/Func/IR/FuncOps.h"
#include "mlir/IR/PatternMatch.h"
#include "mlir/Pass/Pass.h"
#include "mlir/Pass/PassRegistry.h"
#include "llvm/Support/raw_ostream.h"

using namespace mlir;

namespace codesign {
namespace {

struct LowerMaximumFPass
    : public PassWrapper<LowerMaximumFPass, OperationPass<func::FuncOp>> {

  MLIR_DEFINE_EXPLICIT_INTERNAL_INLINE_TYPE_ID(LowerMaximumFPass)

  void getDependentDialects(DialectRegistry &registry) const override {
    registry.insert<arith::ArithDialect>();
  }

  StringRef getArgument() const final { return "lower-maximumf"; }

  StringRef getDescription() const final {
    return "Lower arith.maximumf to cmpf + select";
  }

  void runOnOperation() override {
    func::FuncOp f = getOperation();
    OpBuilder b(&getContext());
    int64_t rewrites = 0;

    f.walk([&](Operation *op) {
      // Match arith.maximumf by name
      if (op->getName().getStringRef() != "arith.maximumf")
        return;

      Value lhs = op->getOperand(0);
      Value rhs = op->getOperand(1);
      auto loc = op->getLoc();

      b.setInsertionPoint(op);

      // cmpf ogt, %lhs, %rhs
      Value cmp =
          b.create<arith::CmpFOp>(loc, arith::CmpFPredicate::OGT, lhs, rhs);

      // select %cmp, %lhs, %rhs
      Value sel = b.create<arith::SelectOp>(loc, cmp, lhs, rhs);

      op->getResult(0).replaceAllUsesWith(sel);
      op->erase();
      ++rewrites;
    });

    llvm::errs() << "[LowerMaximumF] " << f.getName() << ": rewrote "
                 << rewrites << " arith.maximumf ops\n";
  }
};

} // namespace

std::unique_ptr<mlir::Pass> createLowerMaximumFPass() {
  return std::make_unique<LowerMaximumFPass>();
}

void registerCodeSignPasses() {
  // This makes -lower-maximumf available on the command line.
  static PassRegistration<LowerMaximumFPass> reg;
}

} // namespace codesign
