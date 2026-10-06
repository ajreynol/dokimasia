; seq.unit of constant
; EXPECT: unsat
(set-logic ALL)
(declare-const a (Seq Int))
(declare-const b (Seq Int))
(declare-const c (Seq Int))
(declare-const n Int)
(declare-const m Int)
(declare-const e Int)
(assert (not (= (seq.++ (seq.unit 1) a) (seq.++ (seq.unit 1) a))))
(assert (not (= (seq.len (seq.unit 1)) 1)))
(check-sat)
