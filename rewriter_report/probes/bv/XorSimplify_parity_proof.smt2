; XorSimplify: mixed parity x^x^~x^y -> ~x^y (pos even, neg odd)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (not (= (bvxor x x (bvnot x) y) (bvxor (bvnot x) y))))
(check-sat)
