; substr(abc++x, 1, n) strips partially into constant: = substr(bc++x, 0, n)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const n Int)
(assert (not (= (str.substr (str.++ "abc" x) 1 n) (str.substr (str.++ "bc" x) 0 n))))
(check-sat)
