; sequence version: inner unit-const overlapping pattern must not split
; EXPECT: sat
(set-logic ALL)
(declare-const s (Seq Int))
(declare-const t (Seq Int))
(assert (seq.contains (seq.++ s (seq.++ (seq.unit 1) (seq.unit 2)) t) (seq.++ (seq.unit 2) (seq.unit 3))))
(assert (not (seq.contains s (seq.++ (seq.unit 2) (seq.unit 3)))))
(assert (not (seq.contains t (seq.++ (seq.unit 2) (seq.unit 3)))))
(check-sat)
