; "ab"++x in inter(a.Sigma*, Sigma*.c) with x="c": sat
; EXPECT: sat
(set-logic ALL)
(declare-const x String)(declare-const y String)
(assert (str.in_re (str.++ "ab" x) (re.inter (re.++ (str.to_re "a") (re.* re.allchar)) (re.++ (re.* re.allchar) (str.to_re "c")))))(assert (= x "c"))
(check-sat)
