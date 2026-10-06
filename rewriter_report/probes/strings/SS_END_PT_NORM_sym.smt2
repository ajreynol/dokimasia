; length beyond end normalized to len
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.substr x n (+ (str.len x) 1)) (str.substr x n (str.len x)))))
(check-sat)
