; substr(x++y++z, len x + len y + 1, n) = substr(z, 1, n)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const n Int)
(assert (not (= (str.substr (str.++ x y z) (+ (str.len x) (str.len y) 1) n) (str.substr z 1 n))))
(check-sat)
