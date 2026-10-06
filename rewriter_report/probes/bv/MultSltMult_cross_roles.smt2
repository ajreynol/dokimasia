; #13039 variant: L = zext(x+1)*sext(a), R = zext(a)*sext(x) (a zext'd on the right only); C++ accepts via mr[0]==a. Witness x=#b11,a=#b01: slt is false, C++ result true.
; EXPECT: sat
(set-logic QF_BV)
(declare-const a (_ BitVec 2))
(declare-const x (_ BitVec 2))
(assert (and (= a #b01) (= x #b11)
  (not (bvslt (bvmul ((_ zero_extend 2) (bvadd x #b01)) ((_ sign_extend 2) a))
              (bvmul ((_ zero_extend 2) a) ((_ sign_extend 2) x))))))
(check-sat)
