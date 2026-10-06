; seq prefixof single element
; EXPECT: unsat
(set-logic ALL)
(declare-const a (Seq Int))
(declare-const b (Seq Int))
(declare-const c (Seq Int))
(declare-const n Int)
(declare-const m Int)
(declare-const e Int)
(assert (not (= (seq.prefixof a (seq.unit 1)) (seq.contains (seq.unit 1) a))))
(check-sat)
