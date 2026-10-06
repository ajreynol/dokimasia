; Proof probe (--bv-rw-extend-eq): sext(m,x) = c for c with consistent sign bits (-> x=c_lo) and inconsistent ones (-> false).
; EXPECT: unsat
; CVC5-OPTS: --bv-rw-extend-eq
(set-logic QF_BV)
(declare-const x (_ BitVec 3))
(declare-const y (_ BitVec 3))
(declare-const z (_ BitVec 3))
(assert (= ((_ sign_extend 2) x) #b11101))
(assert (or (= ((_ sign_extend 2) y) #b01101) (= #b10101 ((_ sign_extend 2) z)) (not (= x #b101))))
(check-sat)
