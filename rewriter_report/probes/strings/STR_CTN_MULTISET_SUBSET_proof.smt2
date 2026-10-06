; contains(a++x, x++b) ---> false by multiset of chars
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (not (= (str.contains (str.++ "a" x) (str.++ x "b")) false)))
(check-sat)
