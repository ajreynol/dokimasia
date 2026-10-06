; Differential: urem by 0 is identity, so (bvugt (bvurem t 0) 0) holds for t=1 (width 1).
; EXPECT: sat
(set-logic QF_BV)
(declare-const t (_ BitVec 1))
(declare-const x (_ BitVec 1))
(assert (and (= t #b1) (= x #b0) (bvugt (bvurem t x) x)))
(check-sat)
