; seq: len(rev x) = len x
; EXPECT: unsat
(set-logic ALL)
(declare-const x (Seq Int))
(declare-const y (Seq Int))
(declare-const n Int)
(assert (not (= (seq.len (seq.rev x)) (seq.len x))))
(check-sat)
