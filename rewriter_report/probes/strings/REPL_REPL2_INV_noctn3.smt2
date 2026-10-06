; replace x (replace y z w) u with x lacking z,w
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace "ab" (str.replace y "c" "d") w) (str.replace "ab" y w))))
(check-sat)
