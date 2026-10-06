; update a symbolic-length component exactly
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.update (str.++ x "ab" y) (str.len x) "cd") (str.++ x "cd" y))))
(check-sat)
