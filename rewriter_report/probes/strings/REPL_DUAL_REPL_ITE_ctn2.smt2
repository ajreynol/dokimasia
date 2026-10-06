; dual replace ite via y,z mutual non-containment
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace x (str.replace x "a" "b") w) (ite (str.contains x "a") x w))))
(check-sat)
