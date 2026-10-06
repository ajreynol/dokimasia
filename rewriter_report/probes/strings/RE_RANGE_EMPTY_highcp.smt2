; range with high code points reversed is empty
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (str.in_re x (re.range "\u{2ffff}" "\u{10}")))
(check-sat)
