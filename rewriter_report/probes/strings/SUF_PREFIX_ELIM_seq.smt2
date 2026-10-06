; seq suffixof elim
; EXPECT: unsat
(set-logic ALL)
(declare-const a (Seq Int))
(declare-const b (Seq Int))
(declare-const c (Seq Int))
(declare-const n Int)
(declare-const m Int)
(declare-const e Int)
(assert (not (= (seq.suffixof a b) (= a (seq.extract b (- (seq.len b) (seq.len a)) (seq.len a))))))
(check-sat)
