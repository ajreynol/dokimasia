; NotIdemp: ~~~~x -> x (loop)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvnot (bvnot (bvnot (bvnot x)))) x)))
(check-sat)
