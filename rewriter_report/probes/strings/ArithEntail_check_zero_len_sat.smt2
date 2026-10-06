; substr with length -len(y) is NOT always empty? (length 0 when y empty -> empty; check boundary sat side)
; EXPECT: sat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (= (str.substr x 0 (- 1 (str.len y))) "a"))
(check-sat)
