; strip endpoints of contains
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.contains (str.++ "c" x "d") "ab") (str.contains x "ab"))))
(check-sat)
