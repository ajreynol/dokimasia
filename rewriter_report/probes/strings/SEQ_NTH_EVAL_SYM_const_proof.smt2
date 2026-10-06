; seq.nth 2 of const[1,2] ++ unit a ++ t is a (const strip)
; EXPECT: unsat
(set-logic ALL)
(declare-const s (Seq Int))
(declare-const t (Seq Int))
(declare-const a Int)
(declare-const b Int)
(assert (not (= (seq.nth (seq.++ (seq.++ (seq.unit 1) (seq.unit 2)) (seq.unit a) t) 2) a)))
(check-sat)
