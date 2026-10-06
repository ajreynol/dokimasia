; substr(ab++x++y, len x + 2, n) = substr(y, 0, n)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const n Int)
(assert (not (= (str.substr (str.++ "ab" x y) (+ (str.len x) 2) n) (str.substr y 0 n))))
(check-sat)
