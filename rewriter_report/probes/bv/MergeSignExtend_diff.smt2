; Differential: sext of zext(1, x) with x msb=1 must be zero-filled (sext(2,zext(1,#b100)) = #b000100).
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 3))
(assert (and (= x #b100) (not (= ((_ sign_extend 2) ((_ zero_extend 1) x)) #b000100))))
(check-sat)
