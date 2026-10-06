; contains(x++y++z, y++z) and contains(x++"abc"++y, "b")
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (or (not (str.contains (str.++ x y z) (str.++ y z))) (not (str.contains (str.++ x "abc" y) "b"))))
(check-sat)
