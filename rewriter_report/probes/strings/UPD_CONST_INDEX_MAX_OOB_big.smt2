; update at index > 2^32-1
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.update "abc" 4294967296 x) "abc")))
(check-sat)
