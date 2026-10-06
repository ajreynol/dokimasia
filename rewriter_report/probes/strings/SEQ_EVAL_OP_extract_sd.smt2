; seq.extract on constant: negative start, overlong length, start=len
; EXPECT: unsat
(set-logic ALL)
(declare-const s (Seq Int))(declare-const t (Seq Int))(declare-const i Int)
(assert (= s (seq.++ (seq.unit 1) (seq.unit 2) (seq.unit 3))))(assert (or (not (= (seq.extract s (- 1) 2) (as seq.empty (Seq Int)))) (not (= (seq.extract s 1 10) (seq.++ (seq.unit 2) (seq.unit 3)))) (not (= (seq.extract s 3 1) (as seq.empty (Seq Int))))))
(check-sat)
