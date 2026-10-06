; len(from_int(len x + 1)) <= len x + 1 (x>0 case)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (> (str.len (str.from_int (+ (str.len x) 1))) (+ (str.len x) 1)))
(check-sat)
