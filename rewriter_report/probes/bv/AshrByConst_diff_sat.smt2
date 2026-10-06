; AshrByConst: differential, (bvashr x 2) = #xE0 is sat (x=#x80..#x83)
; EXPECT: sat
(set-logic QF_BV)
(declare-const x (_ BitVec 8))
(assert (= (bvashr x #x02) #xE0))
(check-sat)
