; a++x in (a|ab)++c*: x=bc sat; union branches disagree
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (str.in_re (str.++ "a" x) (re.++ (re.union (str.to_re "a") (str.to_re "ab")) (re.* (str.to_re "c")))))
(assert (not (str.in_re x (re.* (str.to_re "c")))))
(check-sat)
