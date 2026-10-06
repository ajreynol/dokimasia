; seq: x = replace(x,[1],[2]) <=> not contains(x,[1])
; EXPECT: unsat
(set-logic ALL)
(declare-const x (Seq Int))
(declare-const y (Seq Int))
(declare-const n Int)
(assert (not (= (= x (seq.replace x (seq.unit 1) (seq.unit 2))) (not (seq.contains x (seq.unit 1))))))
(check-sat)
