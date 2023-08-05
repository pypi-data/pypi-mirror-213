from puan_pv_rs import (
	Disjunction, 
	ConjunctiveComposition, 
	ConjunctiveCompositionKeys, 
	CCKeysIterable,
)

import random
random.seed(0)
n = 100_000
ccs = CCKeysIterable(
	list(
		map(
			lambda _: ConjunctiveCompositionKeys(
				ConjunctiveComposition(
					[
						Disjunction([0,1]),
						Disjunction([0,2]),
					],
					[3,4,5]
				),
				list(
					map(
						lambda _: random.randint(0,100),
						range(6)
					)
				),
			),
			range(n)
		)
	)
)

import time
start = time.time()
evaluated = ccs.evaluate([0,1,2,3,4,5])
print(f"Time elapsed: {time.time() - start} seconds")