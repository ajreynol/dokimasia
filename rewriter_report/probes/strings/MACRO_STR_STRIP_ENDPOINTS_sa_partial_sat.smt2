; contains(ab++x, b) is true; stripping all of ab would be wrong
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (str.contains (str.++ "ab" x) (str.++ "b" y))))
(assert (= y ""))
(check-sat)
