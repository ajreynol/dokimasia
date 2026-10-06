; seq constant: replace([1;2;1;2],[2;1],[3]) = [1;3;2]; replace_all
; EXPECT: unsat
(set-logic ALL)
(assert (not (and (= (seq.replace (seq.++ (seq.unit 1) (seq.unit 2) (seq.unit 1) (seq.unit 2)) (seq.++ (seq.unit 2) (seq.unit 1)) (seq.unit 3)) (seq.++ (seq.unit 1) (seq.unit 3) (seq.unit 2))) (= (seq.replace_all (seq.++ (seq.unit 1) (seq.unit 2) (seq.unit 1) (seq.unit 2)) (seq.unit 2) (seq.++ (seq.unit 5) (seq.unit 5))) (seq.++ (seq.unit 1) (seq.unit 5) (seq.unit 5) (seq.unit 1) (seq.unit 5) (seq.unit 5))) (= (seq.replace (seq.++ (seq.unit 1) (seq.unit 2)) (as seq.empty (Seq Int)) (seq.unit 9)) (seq.++ (seq.unit 9) (seq.unit 1) (seq.unit 2))))))
(check-sat)
