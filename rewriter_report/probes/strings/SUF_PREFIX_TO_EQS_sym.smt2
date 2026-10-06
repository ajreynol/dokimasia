; prefix at least as long -> equality
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.suffixof (str.++ y x) x) (= (str.++ y x) x))))
(check-sat)
