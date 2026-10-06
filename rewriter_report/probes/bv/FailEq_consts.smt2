; FailEq/SimplifyEq/ReflexivityEq: distinct constants equal is false; x=x true; symmetric orientation.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 3))
(declare-const y (_ BitVec 3))
(assert (or (= #b01 #b10) (not (= x x)) (not (= (= x y) (= y x)))))
(check-sat)
