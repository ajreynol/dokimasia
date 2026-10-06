; ExtractConcat across three concat children: ((_ extract 9 2) (concat a b c)) with 4-bit a,b,c.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const a (_ BitVec 4))
(declare-const b (_ BitVec 4))
(declare-const c (_ BitVec 4))
(assert (not (= ((_ extract 9 2) (concat a b c)) (concat ((_ extract 1 0) a) b ((_ extract 3 2) c)))))
(check-sat)
