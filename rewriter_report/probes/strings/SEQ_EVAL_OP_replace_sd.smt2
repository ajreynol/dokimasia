; seq.replace on constants: empty pattern prepends; not found
; EXPECT: unsat
(set-logic ALL)
(declare-const s (Seq Int))(declare-const t (Seq Int))(declare-const i Int)
(assert (= s (seq.++ (seq.unit 1) (seq.unit 2) (seq.unit 3))))(assert (or (not (= (seq.replace s (as seq.empty (Seq Int)) (seq.unit 9)) (seq.++ (seq.unit 9) (seq.++ (seq.unit 1) (seq.unit 2) (seq.unit 3))))) (not (= (seq.replace s (seq.unit 7) (seq.unit 9)) s))))
(check-sat)
