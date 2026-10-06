; ExtractConcat in pre-rewrite over an unflattened concat with constant children (crosses nested boundaries).
; EXPECT: unsat
(set-logic QF_BV)
(declare-const a (_ BitVec 2))
(declare-const b (_ BitVec 3))
(assert (not (= ((_ extract 6 2) (concat (concat a #b10) (concat #b1 b))) (concat ((_ extract 0 0) a) #b101 ((_ extract 2 2) b)))))
(check-sat)
