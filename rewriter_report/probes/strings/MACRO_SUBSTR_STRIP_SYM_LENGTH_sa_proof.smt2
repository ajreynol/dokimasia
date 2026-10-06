; substr(x++y, len x, n) = substr(y, 0, n)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (= (str.substr (str.++ x y) (str.len x) n) (str.substr y 0 n))))
(check-sat)
