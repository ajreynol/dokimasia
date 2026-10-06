; seq: replace(x,[1],[n]) = [n] <=> x=[1] or x=[n]
; EXPECT: unsat
(set-logic ALL)
(declare-const x (Seq Int))
(declare-const y (Seq Int))
(declare-const n Int)
(assert (not (= (= (seq.replace x (seq.unit 1) (seq.unit n)) (seq.unit n)) (or (= x (seq.unit 1)) (= x (seq.unit n))))))
(check-sat)
