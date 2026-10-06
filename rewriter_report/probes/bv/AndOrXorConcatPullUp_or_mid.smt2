; AndOrXorConcatPullUp (or): one constant in middle (macro + pullup3)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 8))
(declare-const a (_ BitVec 2))
(declare-const b (_ BitVec 2))
(declare-const y (_ BitVec 8))
(assert (not (= (bvor x (concat a #x1 b)) (concat (bvor ((_ extract 7 6) x) a) (bvor ((_ extract 5 2) x) #x1) (bvor ((_ extract 1 0) x) b)))))
(check-sat)
