; char in (str.to_re y)* iff y = char
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (str.in_re "A" (re.* (str.to_re y))) (= y "A"))))
(check-sat)
