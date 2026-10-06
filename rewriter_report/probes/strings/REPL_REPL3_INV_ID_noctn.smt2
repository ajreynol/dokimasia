; replace x y (replace y z w) with x lacking z
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace "ab" y (str.replace y "c" w)) "ab")))
(check-sat)
