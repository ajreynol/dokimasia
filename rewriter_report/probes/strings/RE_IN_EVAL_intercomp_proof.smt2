; const membership in inter/comp evaluates false
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (str.in_re "ab" (re.inter (re.* (re.range "a" "b")) (re.comp (str.to_re "ab")))))
(check-sat)
