; substr from 0 covering first component plus part
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.substr (str.++ x y) 0 (+ (str.len x) 1)) (str.++ x (str.substr y 0 1)))))
(check-sat)
