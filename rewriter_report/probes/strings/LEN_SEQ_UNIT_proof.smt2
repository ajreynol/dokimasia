; seq: len(unit n) = 1
; EXPECT: unsat
(set-logic ALL)
(declare-const x (Seq Int))
(declare-const y (Seq Int))
(declare-const n Int)
(assert (not (= (seq.len (seq.unit n)) 1)))
(check-sat)
