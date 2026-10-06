; len(x++ab++y) = len x + 2 + len y
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const u String)
(assert (not (= (str.len (str.++ x "ab" y)) (+ (str.len x) 2 (str.len y)))))
(check-sat)
