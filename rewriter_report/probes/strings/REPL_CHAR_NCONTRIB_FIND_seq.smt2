; seq replace unit in a++a
; EXPECT: unsat
(set-logic ALL)
(declare-const a (Seq Int))
(declare-const b (Seq Int))
(declare-const c (Seq Int))
(declare-const n Int)
(declare-const m Int)
(declare-const e Int)
(assert (not (= (seq.replace (seq.++ a a) (seq.unit e) b) (seq.++ (seq.replace a (seq.unit e) b) a))))
(check-sat)
