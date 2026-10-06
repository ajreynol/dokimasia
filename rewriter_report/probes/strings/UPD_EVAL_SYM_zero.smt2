; update at 0 of exact-length head component
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.update (str.++ "ab" y) 0 "cd") (str.++ "cd" y))))
(check-sat)
