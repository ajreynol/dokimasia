; seq const find
; EXPECT: unsat
(set-logic ALL)
(declare-const a (Seq Int))
(declare-const b (Seq Int))
(declare-const c (Seq Int))
(declare-const n Int)
(declare-const m Int)
(declare-const e Int)
(assert (not (= (seq.replace (seq.++ (seq.unit 1) (seq.unit 2) a) (seq.unit 2) b) (seq.++ (seq.unit 1) b a))))
(check-sat)
