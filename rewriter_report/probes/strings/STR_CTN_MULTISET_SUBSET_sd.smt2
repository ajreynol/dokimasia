; contains(x++"a", "aa"++x)=false (multiset)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (str.contains (str.++ x "a") (str.++ "a" "b" x)))
(check-sat)
