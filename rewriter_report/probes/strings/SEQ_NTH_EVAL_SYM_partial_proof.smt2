; seq.nth 1 of const[1,2] ++ unit a: partial const strip must not yield a
; EXPECT: unsat
(set-logic ALL)
(declare-const s (Seq Int))
(declare-const t (Seq Int))
(declare-const a Int)
(declare-const b Int)
(assert (not (= (seq.nth (seq.++ (seq.++ (seq.unit 1) (seq.unit 2)) (seq.unit a) t) 1) 2)))
(check-sat)
