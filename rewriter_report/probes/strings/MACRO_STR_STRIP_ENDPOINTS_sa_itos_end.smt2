; strip from_int at end: contains(x++from_int(n), 1b) = contains(x, 1b)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.contains (str.++ x (str.from_int n)) "1b") (str.contains x "1b"))))
(check-sat)
