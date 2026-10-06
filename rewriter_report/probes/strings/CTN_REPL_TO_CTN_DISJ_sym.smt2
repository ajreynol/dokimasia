; contains (replace x y z) z
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.contains (str.replace x y z) z) (or (str.contains x y) (str.contains x z)))))
(check-sat)
