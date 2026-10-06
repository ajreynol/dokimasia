; re.loop 2 2 is concat
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (not (= (str.in_re x ((_ re.loop 2 2) (str.to_re y))) (= x (str.++ y y)))))
(check-sat)
