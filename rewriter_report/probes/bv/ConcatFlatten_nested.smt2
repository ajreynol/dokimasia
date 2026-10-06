; ConcatFlatten: nested concats (left and right nesting) flatten to one n-ary concat.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const a (_ BitVec 2))
(declare-const b (_ BitVec 3))
(declare-const c (_ BitVec 1))
(declare-const d (_ BitVec 2))
(assert (not (= (concat (concat a (concat b c)) d) (concat a b c d))))
(check-sat)
