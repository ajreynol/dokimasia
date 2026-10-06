; XorSimplify parity: pos=2,neg=3 -> ~x^y; pos=3,neg=1 -> ones^y = ~y
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (or (not (= (bvxor x (bvnot x) x (bvnot x) (bvnot x) y) (bvxor (bvnot x) y))) (not (= (bvxor x x x (bvnot x) y) (bvnot y)))))
(check-sat)
