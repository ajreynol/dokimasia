; LshrByConst: amount 1 -> concat(0, extract 3 1 x)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvlshr x #x1) (concat #b0 ((_ extract 3 1) x)))))
(check-sat)
