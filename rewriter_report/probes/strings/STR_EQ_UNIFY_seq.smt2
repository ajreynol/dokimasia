; seq: [1;2]++x = [1]++y <=> [2]++x = y
; EXPECT: unsat
(set-logic ALL)
(declare-const x (Seq Int))
(declare-const y (Seq Int))
(assert (not (= (= (seq.++ (seq.unit 1) (seq.unit 2) x) (seq.++ (seq.unit 1) y)) (= (seq.++ (seq.unit 2) x) y))))
(check-sat)
