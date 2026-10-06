; contains concat char splits
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.contains (str.++ x y) "a") (or (str.contains x "a") (str.contains y "a")))))
(check-sat)
