; substr(x, len x + len(from_int(len y)) - 1, n): len(from_int(k))>=1 for k>=0
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.substr x (- (+ (str.len x) (str.len (str.from_int (str.len y)))) 1) n) "")))
(check-sat)
