; ExtractConcat: extract crossing three concat children (partial top, full middle, partial bottom).
; EXPECT: unsat
(set-logic QF_BV)
(declare-const a (_ BitVec 3))
(declare-const b (_ BitVec 3))
(declare-const c (_ BitVec 3))
(assert (not (= ((_ extract 6 1) (concat a b c)) (concat ((_ extract 0 0) a) b ((_ extract 2 1) c)))))
(check-sat)
