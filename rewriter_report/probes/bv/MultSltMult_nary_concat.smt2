; #13039 variant (PR #13042 test 2 shape): n-ary concat(#b00, x+1, z) read as zext(x+1); overflow possible. Witness x=#b01,z=#b11,z2=#b00,a=#b011: slt true, C++ false.
; EXPECT: sat
(set-logic QF_BV)
(declare-const a (_ BitVec 3))
(declare-const x (_ BitVec 2))
(declare-const z (_ BitVec 2))
(declare-const z2 (_ BitVec 2))
(assert (and (= a #b011) (= x #b01) (= z #b11) (= z2 #b00)
  (bvslt (bvmul (concat #b00 (bvadd x #b01) z) ((_ sign_extend 3) a))
         (bvmul (concat #b00 x z2) ((_ sign_extend 3) a)))))
(check-sat)
