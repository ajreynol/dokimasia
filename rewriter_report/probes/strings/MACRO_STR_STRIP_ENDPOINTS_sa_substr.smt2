; contains(substr(abc,n,m), d) is false (substr-of-constant component)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(declare-const m Int)
(assert (str.contains (str.substr "abc" n m) "d"))
(check-sat)
