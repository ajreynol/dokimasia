; replace with possibly-empty pattern must not pull endpoints
; EXPECT: sat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace (str.++ "b" x "b") y z) (str.++ "b" (str.replace x y z) "b"))))
(assert (not (str.contains "b" y)))
(check-sat)
