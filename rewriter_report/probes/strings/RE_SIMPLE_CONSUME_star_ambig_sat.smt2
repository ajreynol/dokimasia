; a++x in (a|ab)* with x=b true but x not in (a|ab)*: must stay sat
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (str.in_re (str.++ "a" x) (re.* (re.union (str.to_re "a") (str.to_re "ab")))))
(assert (not (str.in_re x (re.* (re.union (str.to_re "a") (str.to_re "ab"))))))
(check-sat)
