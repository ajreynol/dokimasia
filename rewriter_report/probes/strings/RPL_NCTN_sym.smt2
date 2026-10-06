; replace when not contained
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace (str.++ "ab" x) (str.++ x "c" x "ab") y) (str.++ "ab" x))))
(check-sat)
