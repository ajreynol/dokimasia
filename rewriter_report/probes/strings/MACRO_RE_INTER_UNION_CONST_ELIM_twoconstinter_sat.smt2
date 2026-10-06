; inter of two distinct consts with R is empty even though each is in R
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (str.in_re x (re.inter (str.to_re "ab") (str.to_re "ba") (re.* (re.range "a" "b")))))
(check-sat)
