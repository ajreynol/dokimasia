; substr(x++y, len x - 1, 2) is not stripped to y: x=ab,y=cd gives bc
; EXPECT: sat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (= x "ab"))
(assert (= y "cd"))
(assert (= (str.substr (str.++ x y) (- (str.len x) 1) 2) "bc"))
(check-sat)
