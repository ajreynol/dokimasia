; seq constant: contains/prefixof/suffixof/rev
; EXPECT: unsat
(set-logic ALL)
(assert (not (and (seq.contains (seq.++ (seq.unit 1) (seq.unit 2) (seq.unit 3)) (seq.++ (seq.unit 2) (seq.unit 3))) (not (seq.contains (seq.++ (seq.unit 1) (seq.unit 2) (seq.unit 3)) (seq.++ (seq.unit 3) (seq.unit 2)))) (seq.prefixof (seq.++ (seq.unit 1) (seq.unit 2)) (seq.++ (seq.unit 1) (seq.unit 2) (seq.unit 3))) (seq.suffixof (seq.++ (seq.unit 2) (seq.unit 3)) (seq.++ (seq.unit 1) (seq.unit 2) (seq.unit 3))) (= (seq.rev (seq.++ (seq.unit 1) (seq.unit 2) (seq.unit 3))) (seq.++ (seq.unit 3) (seq.unit 2) (seq.unit 1))))))
(check-sat)
