; XorSimplify: pair x,~x with two constants and non-constant result; elaboration subgoal equiv3 left as MACRO_THEORY_REWRITE_RCONS_SIMPLE
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (not (= (bvxor x y (bvnot x) #b0000 z #b0001) (bvxor y z #b1110))))
(check-sat)
