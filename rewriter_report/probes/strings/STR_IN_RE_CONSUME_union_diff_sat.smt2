; "a"++x in (a | ab).c : branches differ, x="bc" works
; EXPECT: sat
(set-logic ALL)
(declare-const x String)(declare-const y String)
(assert (str.in_re (str.++ "a" x) (re.++ (re.union (str.to_re "a") (str.to_re "ab")) (str.to_re "c"))))(assert (= x "bc"))
(check-sat)
