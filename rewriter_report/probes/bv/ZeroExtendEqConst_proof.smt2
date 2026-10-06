; Proof probe (--bv-rw-extend-eq): zext(m,x) = c -> x = c_lo or false via ppStaticRewrite (ZeroExtendEqConst / bv-zero-extend-eq-const-1/2).
; EXPECT: unsat
; CVC5-OPTS: --bv-rw-extend-eq
(set-logic QF_BV)
(declare-const x (_ BitVec 3))
(declare-const y (_ BitVec 3))
(assert (= ((_ zero_extend 2) x) #b00101))
(assert (= #b01101 ((_ zero_extend 2) y)))
(check-sat)
