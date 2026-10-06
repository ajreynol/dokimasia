; sequence update symbolic
; EXPECT: unsat
(set-logic ALL)
(declare-const a (Seq Int))
(declare-const b (Seq Int))
(declare-const c (Seq Int))
(declare-const n Int)
(declare-const m Int)
(declare-const e Int)
(assert (not (= (seq.update (seq.++ a (seq.unit 1) b) (seq.len a) (seq.unit 2)) (seq.++ a (seq.unit 2) b))))
(check-sat)
