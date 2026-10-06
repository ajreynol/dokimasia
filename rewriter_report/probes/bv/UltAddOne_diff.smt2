; Differential edge: width 1, y=1 makes y+1 wrap to 0 so x <u y+1 is false; x=0,y=0 makes it true.
; EXPECT: sat
(set-logic QF_BV)
(declare-const x (_ BitVec 1))
(declare-const y (_ BitVec 1))
(assert (bvult x (bvadd y #b1)))
(assert (= x #b0))
(check-sat)
