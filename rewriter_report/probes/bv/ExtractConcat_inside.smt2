; ExtractConcat: extract wholly inside a middle child and exactly one whole child (boundary indices).
; EXPECT: unsat
(set-logic QF_BV)
(declare-const a (_ BitVec 2))
(declare-const b (_ BitVec 3))
(declare-const c (_ BitVec 1))
(assert (not (and (= ((_ extract 3 1) (concat a b c)) b) (= ((_ extract 2 2) (concat a b c)) ((_ extract 1 1) b))
                 (= ((_ extract 0 0) (concat a b c)) c) (= ((_ extract 5 4) (concat a b c)) a))))
(check-sat)
