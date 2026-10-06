; SolveEq (ppStaticRewrite): x+y = x+z --> y = z, trust PP_STATIC_REWRITE expected
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (= (bvadd x y (bvmul z #b0011)) (bvadd x (bvmul z #b0010) #b0001)))
(assert (not (= (bvadd y z) #b0001)))
(check-sat)
