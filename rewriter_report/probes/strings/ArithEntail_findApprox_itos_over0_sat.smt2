; len(from_int(len x)) <= len x is FALSE when x empty (must not be derived)
; EXPECT: sat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (> (str.len (str.from_int (str.len x))) (str.len x)))
(check-sat)
