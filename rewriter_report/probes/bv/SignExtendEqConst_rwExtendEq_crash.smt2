; --bv-rw-extend-eq: ppStaticRewrite returns mkTrustRewrite(atom, null) for any BV equality matching neither Sign/ZeroExtendEqConst -> crash (true answer sat).
; EXPECT: sat
; CVC5-OPTS: --bv-rw-extend-eq
(set-logic QF_BV)
(declare-const x (_ BitVec 3))
(declare-const y (_ BitVec 3))
(assert (not (= x (bvmul y y))))
(check-sat)
