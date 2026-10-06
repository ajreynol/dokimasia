; contains(x++"b"++y, "ab") is NOT the split (overlap)
; EXPECT: sat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.contains (str.++ x "b" y) "ab") (or (str.contains x "ab") (str.contains y "ab")))))
(check-sat)
