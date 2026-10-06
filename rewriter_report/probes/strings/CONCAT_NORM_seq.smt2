; seq: nested concat with units merges to a constant
; EXPECT: unsat
(set-logic ALL)
(declare-const x (Seq Int))
(declare-const y (Seq Int))
(declare-const n Int)
(assert (not (= (seq.++ x (seq.++ (seq.unit 1) (seq.unit 2)) (seq.unit 3)) (seq.++ x (seq.++ (seq.unit 1) (seq.unit 2) (seq.unit 3))))))
(check-sat)
