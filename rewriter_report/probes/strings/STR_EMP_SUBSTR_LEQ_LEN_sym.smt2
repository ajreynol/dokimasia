; "" = substr(x,len y,len z+1) <=> len x <= len y
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= "" (str.substr x (str.len y) (+ (str.len z) 1))) (<= (str.len x) (str.len y)))))
(check-sat)
