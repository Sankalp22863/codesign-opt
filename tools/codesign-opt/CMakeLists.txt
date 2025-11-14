# tools/codesign-opt/CMakeLists.txt

add_mlir_tool(codesign-opt
  codesign-opt.cpp
)

# Give it the same compile flags style as other MLIR tools
llvm_update_compile_flags(codesign-opt)

# Link against your pass lib and the MLIR "driver" libs
target_link_libraries(codesign-opt
  PRIVATE
    CodeSignPasses
    
    # Provides MlirOptMain(...)
    MLIROptLib
    
    # Core MLIR libs
    MLIRParser
    MLIRIR
    MLIRPass
    MLIRSupport
    
    # Individual dialects instead of MLIRInitAllDialects
    MLIRFuncDialect
    MLIRArithDialect
    MLIRAffineDialect
    MLIRSCFDialect
    MLIRMemRefDialect
    MLIRTensorDialect
)

# Optional helper to ensure all needed libs are linked
mlir_check_link_libraries(codesign-opt)
