; symbolic len<=1 pattern
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace (str.++ x x) (str.substr w 0 1) z) (str.++ (str.replace x (str.substr w 0 1) z) x))))
(check-sat)
