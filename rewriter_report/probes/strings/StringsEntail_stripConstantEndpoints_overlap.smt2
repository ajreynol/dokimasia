; contains("abc"++x, "cd"++y) = contains("c"++x, "cd"++y)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.contains (str.++ "abc" x) (str.++ "cd" y)) (str.contains (str.++ "c" x) (str.++ "cd" y)))))
(check-sat)
