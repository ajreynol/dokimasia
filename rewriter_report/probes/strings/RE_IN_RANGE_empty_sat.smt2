; empty string not in range: code("")=-1
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (= x ""))
(assert (str.in_re x (re.range "a" "c")))
(check-sat)
