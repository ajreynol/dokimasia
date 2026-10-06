; seq.indexof on constants: n > len, empty pattern at len, found
; EXPECT: unsat
(set-logic ALL)
(declare-const s (Seq Int))(declare-const t (Seq Int))(declare-const i Int)
(assert (= s (seq.++ (seq.unit 1) (seq.unit 2) (seq.unit 3))))(assert (or (not (= (seq.indexof s (seq.unit 3) 4) (- 1))) (not (= (seq.indexof s (as seq.empty (Seq Int)) 3) 3)) (not (= (seq.indexof s (seq.unit 3) 1) 2))))
(check-sat)
