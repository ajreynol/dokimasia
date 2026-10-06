; substr(x++"abc", n, 1) with end strip: n+1 <= len x not entailed (must keep)
; EXPECT: sat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.substr (str.++ x "abc") 1 1) (str.substr x 1 1))))
(check-sat)
