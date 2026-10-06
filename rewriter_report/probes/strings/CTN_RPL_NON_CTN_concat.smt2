; contains x (replace y z w ++ u) false
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (str.contains "ab" (str.++ (str.replace (str.++ x "c") y "d") z)))
(check-sat)
