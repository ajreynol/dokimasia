; normalize substr length in pattern
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace x (str.++ "a" (str.substr y n (+ (str.len x) 5))) z) (str.replace x (str.++ "a" (str.substr y n (str.len x))) z))))
(check-sat)
