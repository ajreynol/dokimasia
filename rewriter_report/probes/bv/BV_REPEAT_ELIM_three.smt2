; RepeatEliminate: ((_ repeat 3) x) = (concat x x x).
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 2))
(assert (not (= ((_ repeat 3) x) (concat x x x))))
(check-sat)
