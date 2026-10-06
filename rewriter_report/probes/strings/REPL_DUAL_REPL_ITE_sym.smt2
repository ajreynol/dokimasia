; dual replace ite when x lacks z
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace "ab" (str.replace "ab" y "c") w) (ite (str.contains "ab" y) "ab" w))))
(check-sat)
