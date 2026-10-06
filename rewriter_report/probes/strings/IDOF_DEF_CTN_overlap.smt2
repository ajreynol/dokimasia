; def ctn with self-overlapping pattern aa in aaa
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.indexof (str.++ x "aaa" y) "aa" 0) (str.indexof (str.++ x "aa") "aa" 0))))
(check-sat)
