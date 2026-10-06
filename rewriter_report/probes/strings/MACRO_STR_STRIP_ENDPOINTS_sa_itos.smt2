; strip from_int endpoint: contains(from_int(n)++x, a12) = contains(x, a12)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.contains (str.++ (str.from_int n) x) "a12") (str.contains x "a12"))))
(check-sat)
