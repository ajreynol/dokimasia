; ConcatExtractMerge of three adjacent extracts of x plus an unrelated child.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 8))
(declare-const y (_ BitVec 2))
(assert (not (= (concat y ((_ extract 7 6) x) ((_ extract 5 3) x) ((_ extract 2 1) x))
                (concat y ((_ extract 7 1) x)))))
(check-sat)
