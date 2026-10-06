; seq constant: at(s,3) = empty
; EXPECT: unsat
(set-logic ALL)
(assert (not (= (seq.at (seq.++ (seq.unit 1) (seq.unit 2) (seq.unit 3)) 3) (as seq.empty (Seq Int)))))
(check-sat)
