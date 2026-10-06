; RewriteOverflow inline path: all-constant overflow predicates expanded via eliminateOverflows then folded.
; EXPECT: unsat
(set-logic QF_BV)
(assert (not (and (not (bvumulo #x0F #x11)) (bvumulo #x10 #x10) (bvsmulo #x40 #x02) (not (bvsmulo #xF0 #x08))
                  (bvuaddo #xFF #x01) (not (bvsaddo #x7E #x01)) (bvusubo #x00 #x01) (bvssubo #x80 #x01))))
(check-sat)
