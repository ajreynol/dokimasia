; ConcatExtractMerge negative cases: reversed order, gap, different base must NOT merge (differential).
; EXPECT: sat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (distinct (concat ((_ extract 1 0) x) ((_ extract 3 2) x)) x))
(assert (distinct (concat ((_ extract 3 2) x) ((_ extract 0 0) x)) ((_ extract 3 1) x)))
(assert (distinct (concat ((_ extract 3 2) x) ((_ extract 1 0) y)) x))
(check-sat)
