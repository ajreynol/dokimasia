; strip from_int prefix since pattern starts with non-digit
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.indexof (str.++ (str.from_int n) x "a1") "a1" 0) (+ (str.len (str.from_int n)) (str.indexof (str.++ x "a1") "a1" 0)))))
(check-sat)
