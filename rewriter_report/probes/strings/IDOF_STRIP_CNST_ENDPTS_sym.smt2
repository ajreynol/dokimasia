; strip constant prefix that cannot match
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.indexof (str.++ "AB" x "C") "C" 0) (+ 2 (str.indexof (str.++ x "C") "C" 0)))))
(check-sat)
