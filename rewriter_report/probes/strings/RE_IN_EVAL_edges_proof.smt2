; edge const memberships: empty in range, char in loop 0 0, empty in loop 0 2
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (or (str.in_re "" (re.range "a" "b")) (str.in_re "a" ((_ re.loop 0 0) re.allchar)) (not (str.in_re "" ((_ re.loop 0 2) (str.to_re "a")))) (str.in_re "aaa" ((_ re.loop 1 2) (str.to_re "a")))))
(check-sat)
