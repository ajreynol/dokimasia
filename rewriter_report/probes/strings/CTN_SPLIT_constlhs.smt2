; contains const lhs, len<=1 rhs split into disjunction
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.contains "ab" (str.substr x 0 1)) (or (= "" (str.substr x 0 1)) (= "a" (str.substr x 0 1)) (= "b" (str.substr x 0 1))))))
(check-sat)
