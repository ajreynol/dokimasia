; len(from_int(n)) for unconstrained n may be 0 (n<0): must stay sat
; EXPECT: sat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (= (str.len (str.from_int n)) 0))
(check-sat)
