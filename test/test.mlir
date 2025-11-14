// test.mlir
func.func @simple_function(%arg0: i32, %arg1: i32) -> i32 {
  %result = arith.addi %arg0, %arg1 : i32
  return %result : i32
}