; concat in star of fixed-length-1 RE distributes
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (str.in_re (str.++ x "a" y) (re.* (re.range "a" "c"))) (and (str.in_re x (re.* (re.range "a" "c"))) (str.in_re y (re.* (re.range "a" "c")))))))
(check-sat)
