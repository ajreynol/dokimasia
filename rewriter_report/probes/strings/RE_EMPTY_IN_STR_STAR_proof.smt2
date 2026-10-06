; empty string in star of symbolic str.to_re is true
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (str.in_re "" (re.* (str.to_re y)))))
(check-sat)
