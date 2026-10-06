; seq.replace_all with empty pattern is identity; overlapping occurrences
; EXPECT: unsat
(set-logic ALL)
(declare-const s (Seq Int))(declare-const t (Seq Int))(declare-const i Int)
(assert (= s (seq.++ (seq.unit 1) (seq.unit 1) (seq.unit 1))))(assert (or (not (= (seq.replace_all s (as seq.empty (Seq Int)) (seq.unit 5)) s)) (not (= (seq.replace_all s (seq.++ (seq.unit 1) (seq.unit 1)) (seq.unit 5)) (seq.++ (seq.unit 5) (seq.unit 1))))))
(check-sat)
