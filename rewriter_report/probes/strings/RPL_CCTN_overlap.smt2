; pull remainder with overlapping pattern aa in aaa
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace (str.++ x "aaa") "aa" y) (str.++ (str.replace (str.++ x "aa") "aa" y) "a"))))
(check-sat)
