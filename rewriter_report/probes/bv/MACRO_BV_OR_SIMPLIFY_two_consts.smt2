; OrSimplify with two constants and a duplicate negation: (bvor (bvnot x) #b0100 y #b0001 (bvnot x)) = (bvor #b0101 (bvnot x) y).
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvor (bvnot x) #b0100 y #b0001 (bvnot x)) (bvor #b0101 (bvnot x) y))))
(check-sat)
