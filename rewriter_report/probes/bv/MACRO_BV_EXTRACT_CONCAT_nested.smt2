; ExtractConcat over a 5-child concat with a constant child and an extract result spanning four children.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const a (_ BitVec 3))
(declare-const b (_ BitVec 2))
(declare-const c (_ BitVec 3))
(declare-const d (_ BitVec 2))
(assert (not (= ((_ extract 11 1) (concat a #b01 b c d))
                (concat a #b01 b c ((_ extract 1 1) d)))))
(check-sat)
