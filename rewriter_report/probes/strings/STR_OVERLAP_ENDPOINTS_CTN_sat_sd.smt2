; contains("ab"++x, "be"++y) is not contains(x, ...) (overlap b)
; EXPECT: sat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.contains (str.++ "ab" x) (str.++ "be" y)) (str.contains x (str.++ "be" y)))))
(check-sat)
