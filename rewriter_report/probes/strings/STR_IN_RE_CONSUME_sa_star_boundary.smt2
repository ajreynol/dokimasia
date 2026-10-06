; x++ba++y in (ab)* with x=a,y=b (abab) is a member: consume across component boundaries
; EXPECT: sat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (str.in_re (str.++ x "ba" y) (re.* (str.to_re "ab"))))
(assert (= x "a"))
(assert (= y "b"))
(check-sat)
