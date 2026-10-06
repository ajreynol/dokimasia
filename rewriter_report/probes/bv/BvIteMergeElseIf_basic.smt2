; BvIteMergeElseIf: c?(d?x:y):y -> (c&d)?x:y
; EXPECT: unsat
(set-logic QF_BV)
(declare-const c (_ BitVec 1))
(declare-const d (_ BitVec 1))
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(declare-const u (_ BitVec 4))
(assert (not (= (bvite c (bvite d x y) y) (bvite (bvand c d) x y))))
(check-sat)
