; seq: empty = replace(x,y,[n]) <=> x=empty and y!=empty
; EXPECT: unsat
(set-logic ALL)
(declare-const x (Seq Int))
(declare-const y (Seq Int))
(declare-const n Int)
(assert (not (= (= (as seq.empty (Seq Int)) (seq.replace x y (seq.unit n))) (and (= x (as seq.empty (Seq Int))) (not (= y (as seq.empty (Seq Int))))))))
(check-sat)
