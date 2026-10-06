; seq.nth out of bounds is unconstrained: may differ from 0 and from in-range values
; EXPECT: sat
(set-logic ALL)
(declare-const s (Seq Int))
(declare-const t (Seq Int))
(declare-const a Int)
(declare-const b Int)
(assert (not (= (seq.nth (seq.++ (seq.unit 5) (seq.unit 7)) 2) 0)))
(assert (not (= (seq.nth (seq.unit 5) (- 1)) 5)))
(check-sat)
