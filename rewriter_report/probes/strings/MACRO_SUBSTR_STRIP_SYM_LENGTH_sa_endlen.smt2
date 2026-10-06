; substr(x++y, 0, len x + len y + n) with n>=0 is x++y
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const n Int)
(assert (>= n 0))
(assert (not (= (str.substr (str.++ x y) 0 (+ (str.len x) (str.len y) n)) (str.++ x y))))
(check-sat)
