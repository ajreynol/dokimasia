; seq.nth on constant sequence in bounds evaluates
; EXPECT: unsat
(set-logic ALL)
(declare-const s (Seq Int))
(declare-const t (Seq Int))
(declare-const a Int)
(declare-const b Int)
(assert (not (= (seq.nth (seq.++ (seq.unit 5) (seq.unit 7)) 1) 7)))
(check-sat)
