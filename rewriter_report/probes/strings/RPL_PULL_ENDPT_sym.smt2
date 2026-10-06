; pull stripped endpoints out of replace
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace (str.++ "b" x "b") "a" y) (str.++ "b" (str.replace x "a" y) "b"))))
(check-sat)
