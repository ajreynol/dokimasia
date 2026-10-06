; sequence variant: x++[1;2]++y = [2] false
; EXPECT: unsat
(set-logic ALL)
(declare-const x (Seq Int))
(declare-const y (Seq Int))
(assert (not (= (= (seq.++ x (seq.unit 1) (seq.unit 2) y) (seq.unit 2)) false)))
(check-sat)
