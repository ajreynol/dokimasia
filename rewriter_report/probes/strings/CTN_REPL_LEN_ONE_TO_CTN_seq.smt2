; seq contains (replace a b a) unit: exact length 1
; EXPECT: unsat
(set-logic ALL)
(declare-const a (Seq Int))
(declare-const b (Seq Int))
(declare-const c (Seq Int))
(declare-const n Int)
(declare-const m Int)
(declare-const e Int)
(assert (not (= (seq.contains (seq.replace a b a) (seq.unit e)) (seq.contains a (seq.unit e)))))
(check-sat)
