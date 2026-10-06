; seq constant: extract(s,-1,2) = empty
; EXPECT: unsat
(set-logic ALL)
(assert (not (= (seq.extract (seq.++ (seq.unit 1) (seq.unit 2) (seq.unit 3)) (- 1) 2) (as seq.empty (Seq Int)))))
(check-sat)
