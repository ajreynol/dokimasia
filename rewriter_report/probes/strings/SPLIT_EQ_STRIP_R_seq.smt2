; seq: [1]++x++y = x++[1;2]++z <=> [1]++x = x++[1] and y = [2]++z
; EXPECT: unsat
(set-logic ALL)
(declare-const x (Seq Int))
(declare-const y (Seq Int))
(declare-const z (Seq Int))
(assert (not (= (= (seq.++ (seq.unit 1) x y) (seq.++ x (seq.unit 1) (seq.unit 2) z)) (and (= (seq.++ (seq.unit 1) x) (seq.++ x (seq.unit 1))) (= y (seq.++ (seq.unit 2) z))))))
(check-sat)
