set(LLVM_LINK_COMPONENTS
  Support
)

add_mlir_library(CodeSignPasses
  Passes.cpp
  transforms/LowerMaximumF.cpp

  LINK_LIBS PUBLIC
    MLIRIR
    MLIRFuncDialect
    MLIRArithDialect
    MLIRPass
)