; proof: zero_extend 0,1,3 at width 1 (bv-zero-extend-eliminate / -0)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 1))
(assert (or (not (= ((_ zero_extend 0) x) x)) (not (= ((_ zero_extend 1) x) (concat (_ bv0 1) x))) (not (= ((_ zero_extend 3) x) (concat (_ bv0 3) x)))))
(check-sat)
