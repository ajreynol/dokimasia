; contains x (replace y z w) false when x lacks y and w
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (str.contains "ab" (str.replace (str.++ x "c") y "d")))
(check-sat)
