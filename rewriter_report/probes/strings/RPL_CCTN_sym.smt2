; pull remainder past first definite containment
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace (str.++ x "ab") "a" y) (str.++ (str.replace (str.++ x "a") "a" y) "b"))))
(check-sat)
