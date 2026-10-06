; Differential (--bv-rw-extend-eq): sext(1,x)=c at width-1 x and sext(0,..)-like m=1 edge; x=#b1 must satisfy sext(1,x)=#b11.
; EXPECT: sat
; CVC5-OPTS: --bv-rw-extend-eq
(set-logic QF_BV)
(declare-const x (_ BitVec 1))
(declare-const y (_ BitVec 2))
(assert (= ((_ sign_extend 1) x) #b11))
(assert (= ((_ zero_extend 1) y) #b011))
(assert (not (= ((_ sign_extend 1) y) #b001)))
(check-sat)
