; contains("C"++substr("AB",n,m), "CB") can be true (comment case)
; EXPECT: sat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (str.contains (str.++ "C" (str.substr "AB" n m)) "CB"))
(check-sat)
