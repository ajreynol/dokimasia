; "A"++x++y = x++"AB"++z  (SPLIT_EQ_STRIP_R)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (= (str.++ "A" x y) (str.++ x "AB" z)) (and (= (str.++ "A" x) (str.++ x "A")) (= y (str.++ "B" z))))))
(check-sat)
