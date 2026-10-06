; seq const lhs contains unit
; EXPECT: unsat
(set-logic ALL)
(declare-const a (Seq Int))
(declare-const b (Seq Int))
(declare-const c (Seq Int))
(declare-const n Int)
(declare-const m Int)
(declare-const e Int)
(assert (not (= (seq.contains (seq.++ (seq.unit 1) (seq.unit 2)) (seq.unit e)) (or (= (as seq.empty (Seq Int)) (seq.unit e)) (= (seq.unit 1) (seq.unit e)) (= (seq.unit 2) (seq.unit e))))))
(check-sat)
