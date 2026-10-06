; MultPow2: x*y*-2 -> concat(extract 2 0 (-(x*y)), 0)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvmul x y #xE) (concat ((_ extract 2 0) (bvneg (bvmul x y))) #b0))))
(check-sat)
