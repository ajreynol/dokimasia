; OrSimplify: x | ~x -> ones (bv-or-simplify-1/2)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (not (= (bvor y (bvnot x) #b0100 x) #b1111)))
(check-sat)
