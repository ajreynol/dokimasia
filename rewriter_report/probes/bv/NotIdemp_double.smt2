; NotIdemp: ~~x -> x
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvnot (bvnot x)) x)))
(check-sat)
