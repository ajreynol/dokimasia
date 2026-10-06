; LshrByConst: differential, (bvlshr x 8) at width 8 never nonzero
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 8))
(assert (not (= (bvlshr x #x08) #x00)))
(check-sat)
