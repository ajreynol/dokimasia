; ConcatExtractMerge: every split of 4-bit x into adjacent extracts (between y's) re-merges to x.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 1))
(assert (not (and
  (= (concat y ((_ extract 3 1) x) ((_ extract 0 0) x) y) (concat y x y))
  (= (concat y ((_ extract 3 2) x) ((_ extract 1 0) x) y) (concat y x y))
  (= (concat y ((_ extract 3 2) x) ((_ extract 1 1) x) ((_ extract 0 0) x) y) (concat y x y))
  (= (concat y ((_ extract 3 3) x) ((_ extract 2 0) x) y) (concat y x y))
  (= (concat y ((_ extract 3 3) x) ((_ extract 2 1) x) ((_ extract 0 0) x) y) (concat y x y))
  (= (concat y ((_ extract 3 3) x) ((_ extract 2 2) x) ((_ extract 1 0) x) y) (concat y x y))
  (= (concat y ((_ extract 3 3) x) ((_ extract 2 2) x) ((_ extract 1 1) x) ((_ extract 0 0) x) y) (concat y x y)))))
(check-sat)
