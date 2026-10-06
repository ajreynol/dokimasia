; XorSimplify: pair y,~y with one all-ones constant cancels to x (true_count xor ones = 0)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvxor x y (bvnot y) #b1111) x)))
(check-sat)
