; sequence prefix clash [1]++x = [2]++y
; EXPECT: unsat
(set-logic ALL)
(declare-const x (Seq Int))
(declare-const y (Seq Int))
(assert (not (= (= (seq.++ (seq.unit 1) x) (seq.++ (seq.unit 2) y)) false)))
(check-sat)
