; middle constant overlaps pattern: x++b++y contains ab with x=a; split would be wrong
; EXPECT: sat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (str.contains (str.++ x "b" y) "ab"))
(assert (not (str.contains x "ab")))
(assert (not (str.contains y "ab")))
(check-sat)
