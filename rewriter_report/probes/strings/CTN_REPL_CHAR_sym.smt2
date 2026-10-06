; contains replace char when pattern lacks char
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.contains (str.replace x "b" y) "a") (or (str.contains x "a") (and (str.contains x "b") (str.contains y "a"))))))
(check-sat)
