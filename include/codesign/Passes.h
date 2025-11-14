#ifndef CODESIGN_PASSES_H
#define CODESIGN_PASSES_H

#include "mlir/Pass/Pass.h"

namespace codesign {

std::unique_ptr<mlir::Pass> createCodeSignExamplePass();
std::unique_ptr<mlir::Pass> createLowerMaximumFPass();
void registerCodeSignPasses();

} // namespace codesign

#endif // CODESIGN_PASSES_H
