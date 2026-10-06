; seq: x++[1] = [1]++x++z <=> x++[1] = [1]++x and z = empty
; EXPECT: unsat
(set-logic ALL)
(declare-const x (Seq Int))
(declare-const y (Seq Int))
(declare-const z (Seq Int))
(assert (not (= (= (seq.++ x (seq.unit 1)) (seq.++ (seq.unit 1) x z)) (and (= (seq.++ x (seq.unit 1)) (seq.++ (seq.unit 1) x)) (= z (as seq.empty (Seq Int)))))))
(check-sat)
