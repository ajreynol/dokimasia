; contains(substr(abc,n,m), d++y) is false (strip of substr-of-constant sole component, symbolic pattern)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(declare-const m Int)
(assert (str.contains (str.substr "abc" n m) (str.++ "d" y)))
(check-sat)
