; x++y in (a|bc)*: not fixed length 1, x=ab y=c is member though x,y individually not
; EXPECT: sat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (str.in_re (str.++ x y) (re.* (re.union (str.to_re "a") (str.to_re "bc")))))
(assert (= x "ab"))
(assert (= y "c"))
(check-sat)
