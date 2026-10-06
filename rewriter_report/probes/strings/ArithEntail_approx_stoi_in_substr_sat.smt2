; substr start len(x)+to_int(y) is NOT >= len x (to_int may be -1)
; EXPECT: sat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.substr x (+ (str.len x) (str.to_int y)) 1) "")))
(check-sat)
