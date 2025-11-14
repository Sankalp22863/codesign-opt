import re
from pathlib import Path

import re
from pathlib import Path

import re
from pathlib import Path

def rewrite_maximumf_to_generic_cmp_select(input_path: str, output_path: str):
    """
    Rewrite:
        %r = arith.maximumf %a, %b : <ty>
    into:
        %r_tmpN = arith.cmpf ogt, %a, %b : <ty>
        %r      = arith.select %r_tmpN, %a, %b : <ty>

    Uses the custom op syntax to avoid the parser desync that led to:
        error: expected '=' after SSA name
    """
    text = Path(input_path).read_text()

    # Match one-line maximumf: indent, result, lhs, rhs, type
    pat = re.compile(
        r'(?m)^(?P<indent>\s*)'
        r'(?P<res>%[A-Za-z0-9_.]+)\s*=\s*'
        r'arith\.maximumf\s+'
        r'(?P<a>[^,]+?),\s*(?P<b>[^\s:]+)\s*:\s*(?P<ty>[^\n]+?)\s*$'
    )

    counter = 0
    def repl(m):
        nonlocal counter
        g = m.groupdict()
        indent, res = g["indent"], g["res"]
        a, b, ty = g["a"].strip(), g["b"].strip(), g["ty"].strip()
        counter += 1
        tmp = f"{res}_tmp{counter}"

        # Emit custom forms (no quotes, no result type on cmpf)
        #   %tmp = arith.cmpf ogt, %a, %b : ty
        #   %res = arith.select %tmp, %a, %b : ty
        return (
            f"{indent}{tmp} = arith.cmpf ogt, {a}, {b} : {ty}\n"
            f"{indent}{res} = arith.select {tmp}, {a}, {b} : {ty}"
        )

    new_text, n = pat.subn(repl, text)
    if n == 0:
        print("[rewrite] Warning: no arith.maximumf found; wrote input unchanged.")
        new_text = text

    # Normalize line endings just in case
    new_text = new_text.replace("\r\n", "\n").replace("\r", "\n")

    Path(output_path).write_text(new_text + ("" if new_text.endswith("\n") else "\n"))
    print(f"[rewrite] Rewrote {n} maximumf op(s) → custom cmpf+select in {output_path}")



rewrite_maximumf_to_generic_cmp_select("bitnet.mlir", "bitnet_fixed.mlir")