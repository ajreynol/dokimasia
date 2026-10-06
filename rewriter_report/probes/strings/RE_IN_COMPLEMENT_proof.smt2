; x in comp R iff not x in R
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (str.in_re x (re.comp (str.to_re y))) (not (= x y)))))
(check-sat)
