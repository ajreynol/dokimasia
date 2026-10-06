; ConcatConstantMerge: two separate runs of adjacent constants around a variable merge independently.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 3))
(assert (not (= (concat #b01 #b1 x #b0 #b11 #b0) (concat #b011 x #b0110))))
(check-sat)
