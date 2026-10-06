; x++y in (y++x)* is not valid (rotation): sat with x=a,y=b
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (not (str.in_re (str.++ x y) (re.* (str.to_re (str.++ y x))))))
(check-sat)
