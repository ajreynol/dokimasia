; seq.nth (len s + 1) of s++unit a++unit b is b, not a
; EXPECT: unsat
(set-logic ALL)
(declare-const s (Seq Int))
(declare-const t (Seq Int))
(declare-const a Int)
(declare-const b Int)
(assert (not (= (seq.nth (seq.++ s (seq.unit a) (seq.unit b)) (+ (seq.len s) 1)) b)))
(check-sat)
