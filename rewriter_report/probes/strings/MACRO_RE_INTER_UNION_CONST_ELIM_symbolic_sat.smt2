; inter of const with non-const RE is not eliminated; x=ab,y=ab sat
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (str.in_re x (re.inter (str.to_re "ab") (re.* (str.to_re y)))))
(check-sat)
