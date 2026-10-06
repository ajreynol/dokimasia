; seq constant: extract(s,1,10) = [2;3]
; EXPECT: unsat
(set-logic ALL)
(assert (not (= (seq.extract (seq.++ (seq.unit 1) (seq.unit 2) (seq.unit 3)) 1 10) (seq.++ (seq.unit 2) (seq.unit 3)))))
(check-sat)
