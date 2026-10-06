; AshrByConst: differential, x<0 shifted by 9 (width 8) must be #xFF
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 8))
(assert (bvslt x #x00))
(assert (not (= (bvashr x #x09) #xFF)))
(check-sat)
