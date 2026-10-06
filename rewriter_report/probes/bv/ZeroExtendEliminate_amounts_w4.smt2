; proof: zero_extend 0,2 at width 4 (bv-zero-extend-eliminate / -0)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (or (not (= ((_ zero_extend 0) x) x)) (not (= ((_ zero_extend 2) x) (concat (_ bv0 2) x)))))
(check-sat)
