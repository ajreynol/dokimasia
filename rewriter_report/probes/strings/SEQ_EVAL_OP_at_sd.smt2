; seq.at out of range is empty
; EXPECT: unsat
(set-logic ALL)
(declare-const s (Seq Int))(declare-const t (Seq Int))(declare-const i Int)
(assert (= s (seq.++ (seq.unit 1) (seq.unit 2) (seq.unit 3))))(assert (or (not (= (seq.at s 3) (as seq.empty (Seq Int)))) (not (= (seq.at s (- 1)) (as seq.empty (Seq Int)))) (not (= (seq.at s 0) (seq.unit 1)))))
(check-sat)
