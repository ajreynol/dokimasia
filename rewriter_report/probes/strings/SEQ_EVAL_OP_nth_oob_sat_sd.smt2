; seq.nth out of bounds is unspecified: must remain sat for any value
; EXPECT: sat
(set-logic ALL)
(declare-const s (Seq Int))(declare-const t (Seq Int))(declare-const i Int)
(assert (= s (seq.++ (seq.unit 1) (seq.unit 2) (seq.unit 3))))(assert (= (seq.nth s 5) 42))(assert (= (seq.nth s (- 1)) 43))
(check-sat)
