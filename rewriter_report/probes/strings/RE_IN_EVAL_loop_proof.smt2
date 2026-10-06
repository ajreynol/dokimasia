; const membership in loop/allchar evaluates true
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (str.in_re "abab" ((_ re.loop 1 2) (re.++ (str.to_re "a") re.allchar)))))
(check-sat)
