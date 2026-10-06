; combine nested substr, outer window inside inner
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.substr (str.substr x (str.len y) (+ (str.len z) 5)) 1 2) (str.substr x (+ (str.len y) 1) 2))))
(check-sat)
