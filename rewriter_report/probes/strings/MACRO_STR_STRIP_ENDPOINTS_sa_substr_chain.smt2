; contains(substr(abc,n,m)++x, cd): C++ must not strip substr partially
; EXPECT: sat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(declare-const m Int)
(assert (= n 2))
(assert (= m 1))
(assert (= x "d"))
(assert (str.contains (str.++ (str.substr "abc" n m) x) "cd"))
(check-sat)
