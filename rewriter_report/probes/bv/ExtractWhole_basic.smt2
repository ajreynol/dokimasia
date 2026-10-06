; ExtractWhole: extract covering all bits is the identity, also as a concat child.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 5))
(declare-const y (_ BitVec 1))
(assert (not (= (concat ((_ extract 0 0) y) ((_ extract 4 0) x)) (concat y x))))
(check-sat)
