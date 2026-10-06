; #13039 variant: L = zext(a)*sext(x+1), R = zext(x)*sext(a). Witness x=#b10,a=#b01: slt is true, C++ result false.
; EXPECT: sat
(set-logic QF_BV)
(declare-const a (_ BitVec 2))
(declare-const x (_ BitVec 2))
(assert (and (= a #b01) (= x #b10)
  (bvslt (bvmul ((_ zero_extend 2) a) ((_ sign_extend 2) (bvadd x #b01)))
         (bvmul ((_ zero_extend 2) x) ((_ sign_extend 2) a)))))
(check-sat)
