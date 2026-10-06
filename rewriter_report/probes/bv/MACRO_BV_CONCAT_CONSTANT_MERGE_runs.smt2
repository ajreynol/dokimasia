; ConcatConstantMerge of two runs of constants around a variable.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 3))
(assert (not (= (concat #b1 #b0 x #b11 #b0 #b1) (concat #b10 x #b1101))))
(check-sat)
