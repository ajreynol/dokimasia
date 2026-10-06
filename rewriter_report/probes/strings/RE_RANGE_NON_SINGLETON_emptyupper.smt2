; range with symbolic lower, empty upper bound is empty
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (str.in_re x (re.range y "")))
(check-sat)
