; len y - len(from_int(len y)) can be -1 (y empty): substr(x, that + len x, 1) not empty
; EXPECT: sat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.substr x (+ (- (str.len y) (str.len (str.from_int (str.len y)))) (str.len x)) 1) "")))
(check-sat)
