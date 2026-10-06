; ConcatExtractMerge: single-bit extracts x[1]x[0] of a 2-bit x merge to the whole x (then ExtractWhole).
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 2))
(declare-const z (_ BitVec 1))
(assert (not (= (concat z ((_ extract 1 1) x) ((_ extract 0 0) x)) (concat z x))))
(check-sat)
