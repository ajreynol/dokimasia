; seq.nth at 0 of unit a ++ t is a
; EXPECT: unsat
(set-logic ALL)
(declare-const s (Seq Int))
(declare-const t (Seq Int))
(declare-const a Int)
(declare-const b Int)
(assert (not (= (seq.nth (seq.++ (seq.unit a) t) 0) a)))
(check-sat)
