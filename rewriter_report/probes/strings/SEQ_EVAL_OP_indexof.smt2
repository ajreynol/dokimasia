; seq constant: indexof([1;2;1;2],[1;2],1) = 2; from -1 gives -1
; EXPECT: unsat
(set-logic ALL)
(assert (not (and (= (seq.indexof (seq.++ (seq.unit 1) (seq.unit 2) (seq.unit 1) (seq.unit 2)) (seq.++ (seq.unit 1) (seq.unit 2)) 1) 2) (= (seq.indexof (seq.++ (seq.unit 1) (seq.unit 2) (seq.unit 1) (seq.unit 2)) (seq.++ (seq.unit 1) (seq.unit 2)) (- 1)) (- 1)) (= (seq.indexof (seq.++ (seq.unit 1) (seq.unit 2)) (as seq.empty (Seq Int)) 2) 2) (= (seq.indexof (seq.++ (seq.unit 1) (seq.unit 2)) (as seq.empty (Seq Int)) 3) (- 1)))))
(check-sat)
