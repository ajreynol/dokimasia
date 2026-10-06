; substr(w,0,len y) = y++z <=> substr(w,0,len y)=y and z="" (len(lhs)<=len(y) non-syntactic)
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= (str.substr w 0 (str.len y)) (str.++ y z)) (and (= (str.substr w 0 (str.len y)) y) (= z "")))))
(check-sat)
