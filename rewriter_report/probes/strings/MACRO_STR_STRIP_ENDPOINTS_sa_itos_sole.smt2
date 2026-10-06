; contains(from_int(n), a++y) is false (strip sole from_int component)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(declare-const m Int)
(assert (str.contains (str.from_int n) (str.++ "a" y)))
(check-sat)
