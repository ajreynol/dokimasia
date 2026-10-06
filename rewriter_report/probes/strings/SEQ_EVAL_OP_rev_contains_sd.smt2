; seq.rev and seq.contains/prefixof/suffixof on constants
; EXPECT: unsat
(set-logic ALL)
(declare-const s (Seq Int))(declare-const t (Seq Int))(declare-const i Int)
(assert (= s (seq.++ (seq.unit 1) (seq.unit 2) (seq.unit 3))))(assert (or (not (= (seq.rev s) (seq.++ (seq.unit 3) (seq.unit 2) (seq.unit 1)))) (not (seq.contains s (seq.++ (seq.unit 2) (seq.unit 3)))) (seq.prefixof (seq.unit 2) s) (not (seq.suffixof (seq.unit 3) s))))
(check-sat)
