; substr(x,0,len(from_int(len y+1))) vs len y+1 bound: substr(x, len y + 1 - len(from_int(len y + 1)) + len x, n) = ""
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.substr x (+ (- (+ (str.len y) 1) (str.len (str.from_int (+ (str.len y) 1)))) (str.len x)) n) "")))
(check-sat)
