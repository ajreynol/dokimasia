; contains(x++from_int(n), "b1") is NOT contains(x,"b1") (b1 can straddle)
; EXPECT: sat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.contains (str.++ x (str.from_int n)) "b1") (str.contains x "b1"))))
(check-sat)
