; seq.update on constants: in range, at len (no-op), overlong
; EXPECT: unsat
(set-logic ALL)
(declare-const s (Seq Int))(declare-const t (Seq Int))(declare-const i Int)
(assert (= s (seq.++ (seq.unit 1) (seq.unit 2) (seq.unit 3))))(assert (or (not (= (seq.update s 1 (seq.++ (seq.unit 8) (seq.unit 9) (seq.unit 7))) (seq.++ (seq.unit 1) (seq.unit 8) (seq.unit 9)))) (not (= (seq.update s 3 (seq.unit 8)) s))))
(check-sat)
