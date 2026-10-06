; indexof(x++ab, y++a, 0): trailing ab has reverse overlap with pattern; x=,y= gives 0
; EXPECT: sat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (= x ""))
(assert (= y ""))
(assert (= (str.indexof (str.++ x "ab") (str.++ y "a") 0) 0))
(check-sat)
