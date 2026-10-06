; AndOrXorConcatPullUp (or): first concat has const last (C++ splits there), second concat has a middle const
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 8))
(declare-const a (_ BitVec 4))
(declare-const c (_ BitVec 2))
(declare-const d (_ BitVec 2))
(assert (not (= (bvor x (concat a #x0) (concat c #x1 d)) (bvor (concat c #x1 d) (concat a #x0) x))))
(check-sat)
