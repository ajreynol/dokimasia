; BvIteEqualCond: c?(c?x:y):(c?z:u) -> c?x:u
; EXPECT: unsat
(set-logic QF_BV)
(declare-const c (_ BitVec 1))
(declare-const d (_ BitVec 1))
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(declare-const u (_ BitVec 4))
(assert (not (= (bvite c (bvite c x y) (bvite c z u)) (bvite c x u))))
(check-sat)
