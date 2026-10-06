; seq.nth at len(prefix) of prefix++unit a++suffix is a
; EXPECT: unsat
(set-logic ALL)
(declare-const s (Seq Int))
(declare-const t (Seq Int))
(declare-const a Int)
(declare-const b Int)
(assert (not (= (seq.nth (seq.++ s (seq.unit a) t) (seq.len s)) a)))
(check-sat)
