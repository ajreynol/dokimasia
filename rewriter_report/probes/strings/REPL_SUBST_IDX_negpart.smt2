; substr pattern normalization when len t > len x + 1
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace x (str.++ (str.++ x "ab") (str.substr y n (+ 1 (str.len z)))) w) x)))
(check-sat)
