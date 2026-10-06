; x in allchar* is true
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (str.in_re x (re.* re.allchar))))
(check-sat)
