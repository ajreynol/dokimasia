; substr(x, len x + len(from_int(n)) - 1, 1): from_int(n) may be empty (n<0) -> not entailed
; EXPECT: sat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.substr x (- (+ (str.len x) (str.len (str.from_int n))) 1) 1) "")))
(check-sat)
