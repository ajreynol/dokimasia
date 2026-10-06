; NotIdemp: ~~~x -> ~x (loop leaves one)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvnot (bvnot (bvnot x))) (bvnot x))))
(check-sat)
