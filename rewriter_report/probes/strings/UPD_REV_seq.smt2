; sequence update of reverse
; EXPECT: unsat
(set-logic ALL)
(declare-const a (Seq Int))
(declare-const b (Seq Int))
(declare-const c (Seq Int))
(declare-const n Int)
(declare-const m Int)
(declare-const e Int)
(assert (not (= (seq.update (seq.rev a) n (seq.unit 5)) (seq.rev (seq.update a (- (seq.len a) (+ n 1)) (seq.unit 5))))))
(check-sat)
