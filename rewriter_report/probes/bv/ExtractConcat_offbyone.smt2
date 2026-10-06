; ExtractConcat differential: an off-by-one slice (shifted by one bit) must be distinguishable (sat).
; EXPECT: sat
(set-logic QF_BV)
(declare-const a (_ BitVec 3))
(declare-const b (_ BitVec 3))
(declare-const c (_ BitVec 3))
(assert (not (= ((_ extract 6 1) (concat a b c)) (concat ((_ extract 1 0) a) b ((_ extract 2 2) c)))))
(check-sat)
