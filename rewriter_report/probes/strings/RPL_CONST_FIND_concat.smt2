; replace in constant head of concat
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace (str.++ "abab" x) "ba" y) (str.++ "a" y "b" x))))
(check-sat)
