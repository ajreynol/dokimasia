; definite prefix match over multiple components
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace (str.++ "ab" x "cd" y) (str.++ "ab" x "c") z) (str.++ z "d" y))))
(check-sat)
