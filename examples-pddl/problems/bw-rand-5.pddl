(define (problem BW-rand-5)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5  - block)
(:init
(handempty)
(on b1 b5)
(on b2 b1)
(ontable b3)
(on b4 b3)
(on b5 b4)
(clear b2)
)
(:goal
(and
(on b1 b4)
(on b2 b1)
(on b5 b3))
)
)
