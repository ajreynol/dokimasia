; range a..a is str.to_re a
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (str.in_re x (re.range "a" "a")) (= x "a"))))
(check-sat)
