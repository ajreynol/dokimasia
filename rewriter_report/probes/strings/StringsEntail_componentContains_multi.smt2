; contains(w++"xab"++y++"cdz", "ab"++y++"cd") (suffix/prefix of constant endpoints)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (str.contains (str.++ w "xab" y "cdz") (str.++ "ab" y "cd"))))
(check-sat)
