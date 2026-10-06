; AndOrXorConcatPullUp (and): first concat child has a zero constant, second concat present
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 8))
(declare-const a (_ BitVec 4))
(declare-const b (_ BitVec 4))
(assert (not (= (bvand x (concat a #x0) (concat #xF b)) (concat (bvand ((_ extract 7 4) x) a #xF) #x0))))
(check-sat)
