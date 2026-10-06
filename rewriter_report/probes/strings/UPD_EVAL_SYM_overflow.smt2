; update symbolic: replacement longer than component not rewritten wrongly
; EXPECT: sat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.update (str.++ "ab" y) 1 "xyz") (str.++ "axyz" y))))
(check-sat)
