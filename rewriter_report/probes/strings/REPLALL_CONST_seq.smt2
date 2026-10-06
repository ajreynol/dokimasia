; seq replace_all constant
; EXPECT: unsat
(set-logic ALL)
(declare-const a (Seq Int))
(declare-const b (Seq Int))
(declare-const c (Seq Int))
(declare-const n Int)
(declare-const m Int)
(declare-const e Int)
(assert (not (= (seq.replace_all (seq.++ (seq.unit 1) (seq.unit 1) (seq.unit 1)) (seq.++ (seq.unit 1) (seq.unit 1)) (seq.unit 2)) (seq.++ (seq.unit 2) (seq.unit 1)))))
(check-sat)
