; seq constant: update([1;2;3],1,[7;8;9]) = [1;7;8]; update at -1 / at len unchanged
; EXPECT: unsat
(set-logic ALL)
(assert (not (and (= (seq.update (seq.++ (seq.unit 1) (seq.unit 2) (seq.unit 3)) 1 (seq.++ (seq.unit 7) (seq.unit 8) (seq.unit 9))) (seq.++ (seq.unit 1) (seq.unit 7) (seq.unit 8))) (= (seq.update (seq.++ (seq.unit 1) (seq.unit 2) (seq.unit 3)) (- 1) (seq.unit 7)) (seq.++ (seq.unit 1) (seq.unit 2) (seq.unit 3))) (= (seq.update (seq.++ (seq.unit 1) (seq.unit 2) (seq.unit 3)) 3 (seq.unit 7)) (seq.++ (seq.unit 1) (seq.unit 2) (seq.unit 3))))))
(check-sat)
