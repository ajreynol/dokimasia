; contains(x++"ab"++y, "a"++y) is not entailed ("b" in between)
; EXPECT: sat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (str.contains (str.++ x "ab" y) (str.++ "a" y))))
(check-sat)
