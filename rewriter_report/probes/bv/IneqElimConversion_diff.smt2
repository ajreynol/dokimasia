; Differential: negative i wraps mod 2^w; int2bv 2 of -1 is #b11, so (bvule #b10 (int2bv 2 i)) with i=-1 holds.
; EXPECT: sat
(set-logic ALL)
(declare-const i Int)
(assert (= i (- 1)))
(assert (bvule #b10 ((_ int2bv 2) i)))
(assert (bvult ((_ int2bv 2) (- i 2)) #b10))
(check-sat)
