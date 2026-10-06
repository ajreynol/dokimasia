; seq: len(update(x,n,y)) = len x
; EXPECT: unsat
(set-logic ALL)
(declare-const x (Seq Int))
(declare-const y (Seq Int))
(declare-const n Int)
(assert (not (= (seq.len (seq.update x n y)) (seq.len x))))
(check-sat)
