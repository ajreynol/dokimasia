; AndOrXorConcatPullUp (or): ones constant first in concat (pullup rule 2)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 8))
(declare-const a (_ BitVec 2))
(declare-const b (_ BitVec 2))
(declare-const y (_ BitVec 8))
(assert (not (= (bvor x (concat #xF a b)) (concat (bvor ((_ extract 7 4) x) #xF) (bvor ((_ extract 3 0) x) (concat a b))))))
(check-sat)
