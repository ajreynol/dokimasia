; seq: empty = replace(x,[n],empty) <=> prefixof(x,[n]) (symbolic length-one pattern)
; EXPECT: unsat
(set-logic ALL)
(declare-const x (Seq Int))
(declare-const y (Seq Int))
(declare-const n Int)
(assert (not (= (= (as seq.empty (Seq Int)) (seq.replace x (seq.unit n) (as seq.empty (Seq Int)))) (seq.prefixof x (seq.unit n)))))
(check-sat)
