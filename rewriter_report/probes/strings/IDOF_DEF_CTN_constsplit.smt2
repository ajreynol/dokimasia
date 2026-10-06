; def ctn where pattern inside constant component
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.indexof (str.++ x "abc" y) "b" 0) (str.indexof (str.++ x "ab") "b" 0))))
(check-sat)
