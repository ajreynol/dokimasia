; replace_all const with symbolic replacement
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace_all "abab" "b" x) (str.++ "a" x "a" x))))
(check-sat)
