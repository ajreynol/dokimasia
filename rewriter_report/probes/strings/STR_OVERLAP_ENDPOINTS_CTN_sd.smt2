; contains("ab"++x++"cd", "e"++y++"f") = contains(x, ...)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.contains (str.++ "ab" x "cd") (str.++ "e" y "f")) (str.contains x (str.++ "e" y "f")))))
(check-sat)
