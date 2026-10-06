; seq: contains([1]++x, x++[2]) ---> false
; EXPECT: unsat
(set-logic ALL)
(declare-const x (Seq Int))
(declare-const y (Seq Int))
(declare-const n Int)
(assert (not (= (seq.contains (seq.++ (seq.unit 1) x) (seq.++ x (seq.unit 2))) false)))
(check-sat)
