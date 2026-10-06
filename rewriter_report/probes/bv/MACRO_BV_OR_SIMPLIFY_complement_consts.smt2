; OrSimplify with two constants and a complementary pair collapses to ones.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvor x #b0100 y #b0001 (bvnot x)) #b1111)))
(check-sat)
