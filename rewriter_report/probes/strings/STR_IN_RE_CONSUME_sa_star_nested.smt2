; ab++x in (a b*)*: x=bba is a member
; EXPECT: sat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (str.in_re (str.++ "ab" x) (re.* (re.++ (str.to_re "a") (re.* (str.to_re "b"))))))
(assert (= x "bba"))
(check-sat)
