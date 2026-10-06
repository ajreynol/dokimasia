; replace(c++x++d, a, y) = c++replace(x++d? ...) const pattern strips one side at a time
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace (str.++ "c" x "d") "a" y) (str.++ "c" (str.replace x "a" y) "d"))))
(check-sat)
