; a++x in (ab|b)*: x=b is a member (consume must keep the ab branch)
; EXPECT: sat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (str.in_re (str.++ "a" x) (re.* (re.union (str.to_re "ab") (str.to_re "b")))))
(assert (= x "b"))
(check-sat)
