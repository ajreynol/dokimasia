; pattern found but not prefix: must not become z ++ rest
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace (str.++ "ab" x) (str.++ "b" x) z) (str.++ "a" z))))
(check-sat)
