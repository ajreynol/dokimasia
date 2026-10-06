; substr(x++y, len x + n, 1) must not strip x when n may be negative: x=a,y=b,n=-1 gives a
; EXPECT: sat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const n Int)
(assert (= x "a"))
(assert (= y "b"))
(assert (= n (- 1)))
(assert (= (str.substr (str.++ x y) (+ (str.len x) n) 1) "a"))
(check-sat)
