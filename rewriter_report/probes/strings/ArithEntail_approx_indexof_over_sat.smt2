; indexof(x,y,n) can equal len(x) (y empty, n=len x): substr(z, len x - indexof(x,y,n) + len z - 1, 1)
; EXPECT: sat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.substr z (- (+ (- (str.len x) (str.indexof x y n)) (str.len z)) 1) 1) "")))
(check-sat)
