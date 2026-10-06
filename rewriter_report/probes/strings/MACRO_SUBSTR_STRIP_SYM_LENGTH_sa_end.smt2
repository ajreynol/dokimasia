; substr(x++y, 0, len x) = x  (strip end point)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (= (str.substr (str.++ x "ab" y) 0 (+ (str.len x) 1)) (str.++ x "a"))))
(check-sat)
