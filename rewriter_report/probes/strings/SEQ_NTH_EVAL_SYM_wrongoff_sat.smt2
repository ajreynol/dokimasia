; seq.nth (len t) of s++unit a: offset not entailed, sat with a differing
; EXPECT: sat
(set-logic ALL)
(declare-const s (Seq Int))
(declare-const t (Seq Int))
(declare-const a Int)
(declare-const b Int)
(assert (not (= (seq.nth (seq.++ s (seq.unit a) t) (seq.len t)) a)))
(check-sat)
