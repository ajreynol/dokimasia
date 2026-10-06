; range at max code point bounds is satisfiable
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (str.in_re x (re.range "\u{2fffe}" "\u{2ffff}")))
(assert (not (= x "\u{2fffe}")))
(check-sat)
