; from_int endpoint not strippable when pattern starts with a digit: n=1,x=2 contains 12
; EXPECT: sat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(declare-const m Int)
(assert (= n 1))
(assert (= x "2"))
(assert (str.contains (str.++ (str.from_int n) x) "12"))
(check-sat)
