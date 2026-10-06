; MultSimplify edge: width 1, negation dropped (size>1 guard), -1 == 1
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 1))
(declare-const y (_ BitVec 1))
(assert (not (= (bvmul (bvneg x) y #b1) (bvmul x y))))
(check-sat)
