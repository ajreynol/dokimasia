; contains(x++"c"++y, "ab") = contains(x,"ab") or contains(y,"ab")
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.contains (str.++ x "c" y) "ab") (or (str.contains x "ab") (str.contains y "ab")))))
(check-sat)
