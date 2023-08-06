from concurrent.futures import ThreadPoolExecutor
from time import perf_counter

import numpy as np

from hardyweinberg_equilibrium.config import get_logger
from hardyweinberg_equilibrium.utils.generators.population_generator import population_generator

log = get_logger(__name__)


def sample_chunks_generator(samples, nchunks):
    sample_list = []
    for _ in range(0, nchunks):
        sample_list.append(samples)
    return sample_list


# Thread pooling is much faster than asyncio generating chunks
def test_treadpooling_generator():
    generator_list = []
    start = perf_counter()
    with ThreadPoolExecutor() as executor:
        for _ in executor.map(population_generator, [1000]):
            generator_list.append(_.__next__())  # extend the list with the generator
    end = perf_counter()
    generator_list = generator_list[0]
    log.info(f"Generator List: {len(generator_list)}")
    log.info(f"Time Elapsed: {end - start:0.4f} seconds")
    # log.info(f"Generator List Shape: {np.shape(generator_list)}")
    log.info(f"First Chunk: {generator_list[0]}")
    assert len(generator_list) == 1000
