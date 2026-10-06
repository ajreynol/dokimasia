; sequence replace pull remainder
; EXPECT: unsat
(set-logic ALL)
(declare-const a (Seq Int))
(declare-const b (Seq Int))
(declare-const c (Seq Int))
(declare-const n Int)
(declare-const m Int)
(declare-const e Int)
(assert (not (= (seq.replace (seq.++ a (seq.unit 1) (seq.unit 2)) (seq.unit 1) b) (seq.++ (seq.replace (seq.++ a (seq.unit 1)) (seq.unit 1) b) (seq.unit 2)))))
(check-sat)
