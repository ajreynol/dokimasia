; const membership true case for diff/opt: assert true memberships
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (and (str.in_re "ac" (re.diff (re.* (re.range "a" "c")) (str.to_re "ab"))) (str.in_re "" (re.opt (str.to_re "q"))) (str.in_re "b" (re.range "a" "c")) (= x "")))
(check-sat)
