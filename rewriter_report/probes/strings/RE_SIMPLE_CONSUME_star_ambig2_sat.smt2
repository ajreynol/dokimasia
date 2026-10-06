; x++a in (a|ba)* with x=b: consuming one 'a' from back is unsound
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (str.in_re (str.++ x "a") (re.* (re.union (str.to_re "a") (str.to_re "ba")))))
(assert (not (str.in_re x (re.* (re.union (str.to_re "a") (str.to_re "ba"))))))
(check-sat)
