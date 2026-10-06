; contains("abca", x++"c"++y++"a") satisfiable
; EXPECT: sat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (str.contains "abca" (str.++ x "c" y "a")))
(check-sat)
