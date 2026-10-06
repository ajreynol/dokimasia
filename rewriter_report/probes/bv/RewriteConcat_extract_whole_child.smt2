; RewriteConcat applies ExtractWhole to children (ApplyRuleToChildren) then merges.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (concat ((_ extract 3 0) x) y ((_ extract 3 0) y)) (concat x y y))))
(check-sat)
