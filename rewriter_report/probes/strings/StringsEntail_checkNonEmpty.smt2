; replace("a"++x, "", y) = y ++ "a" ++ x and str.at on nonempty
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.replace (str.++ "a" x) "" y) (str.++ y "a" x))))
(check-sat)
