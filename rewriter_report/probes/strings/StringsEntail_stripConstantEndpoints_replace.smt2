; replace("ab"++x++"cd", "e"++y++"f", z) strips endpoints
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.replace (str.++ "ab" x "cd") (str.++ "e" y "f") z) (str.++ "ab" (str.replace x (str.++ "e" y "f") z) "cd"))))
(check-sat)
