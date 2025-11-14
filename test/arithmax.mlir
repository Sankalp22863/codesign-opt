func.func @max_example(%arg0: f32, %arg1: f32) -> f32 {
  %result = arith.maximumf %arg0, %arg1 : f32
  return %result : f32
}