; combine nested substr, inner window shorter
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.substr (str.substr x (str.len y) 3) 1 (+ (str.len z) 2)) (str.substr x (+ (str.len y) 1) 2))))
(check-sat)
