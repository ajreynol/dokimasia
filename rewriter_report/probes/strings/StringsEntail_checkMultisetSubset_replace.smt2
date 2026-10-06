; contains(replace(x,y,"a"), x++"b"++"b") false: multiset of replace(x,y,a)=x,a
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (str.contains (str.replace x y "a") (str.++ x "b")))
(check-sat)
