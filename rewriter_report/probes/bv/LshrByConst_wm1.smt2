; LshrByConst: amount w-1 -> concat(000, extract 3 3 x)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvlshr x #x3) (concat #b000 ((_ extract 3 3) x)))))
(check-sat)
