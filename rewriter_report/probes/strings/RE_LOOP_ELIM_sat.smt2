; x=aaaa not in loop 1 3 of a
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (= x "aaaa"))
(assert (str.in_re x ((_ re.loop 1 3) (str.to_re "a"))))
(check-sat)
