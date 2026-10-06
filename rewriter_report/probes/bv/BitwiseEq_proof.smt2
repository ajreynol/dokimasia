; BitwiseEq (--bitwise-eq, ppStaticRewrite): (bvand a b)=#b1 --> a=1 /\ b=1; comp; neg
; EXPECT: unsat
; CVC5-OPTS: --bitwise-eq
(set-logic QF_BV)
(declare-const x (_ BitVec 1))
(declare-const y (_ BitVec 1))
(declare-const z (_ BitVec 1))
(assert (= (bvand x y z) #b1))
(assert (or (= x #b0) (= (bvcomp y z) #b0) (= (bvneg z) #b0)))
(check-sat)
