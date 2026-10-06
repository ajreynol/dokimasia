; seq constant: update([1;2;3],1,[7]) = [1;7;3] (CPC $seq_eval has no seq.update case)
; EXPECT: unsat
(set-logic ALL)
(assert (not (= (seq.update (seq.++ (seq.unit 1) (seq.unit 2) (seq.unit 3)) 1 (seq.unit 7)) (seq.++ (seq.unit 1) (seq.unit 7) (seq.unit 3)))))
(check-sat)
