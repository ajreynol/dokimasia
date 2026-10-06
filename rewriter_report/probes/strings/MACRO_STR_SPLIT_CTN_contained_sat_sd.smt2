; contains(x++"b"++y, "abc"): t contains c, no split
; EXPECT: sat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.contains (str.++ x "b" y) "abc") (or (str.contains x "abc") (str.contains y "abc")))))
(check-sat)
