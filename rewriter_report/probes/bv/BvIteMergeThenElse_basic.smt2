; BvIteMergeThenElse: c?x:(d?x:y) -> (~c&~d)?y:x
; EXPECT: unsat
(set-logic QF_BV)
(declare-const c (_ BitVec 1))
(declare-const d (_ BitVec 1))
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(declare-const u (_ BitVec 4))
(assert (not (= (bvite c x (bvite d x y)) (bvite (bvand (bvnot c) (bvnot d)) y x))))
(check-sat)
