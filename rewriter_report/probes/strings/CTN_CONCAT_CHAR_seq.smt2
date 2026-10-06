; sequence contains concat single element
; EXPECT: unsat
(set-logic ALL)
(declare-const a (Seq Int))
(declare-const b (Seq Int))
(declare-const c (Seq Int))
(declare-const n Int)
(declare-const m Int)
(declare-const e Int)
(assert (not (= (seq.contains (seq.++ a b) (seq.unit 1)) (or (seq.contains a (seq.unit 1)) (seq.contains b (seq.unit 1))))))
(check-sat)
