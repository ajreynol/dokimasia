; len(from_int(len x)) <= len x + 1 (x>=0 case, boundary 0 -> "0")
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (> (str.len (str.from_int (str.len x))) (+ (str.len x) 1)))
(check-sat)
