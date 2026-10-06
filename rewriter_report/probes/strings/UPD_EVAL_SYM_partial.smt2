; update splitting a constant
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.update (str.++ "abc" y) 1 "x") (str.++ "axc" y))))
(check-sat)
