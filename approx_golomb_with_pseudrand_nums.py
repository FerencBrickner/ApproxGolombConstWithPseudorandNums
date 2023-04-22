from typing import Final, Generator
import logging


def generate_pseudorandom_numbers(
    *, seed: int, multiplier: int, modulus: int, increment: int, SAMPLE_SIZE: Final[int]
) -> Generator[float, None, None]:
    yield from (
        seed := (seed * multiplier + increment) % modulus for _ in SAMPLE_SIZE * "."
    )


def approx_golomb_dickman_constant(
    *,
    SAMPLE_SIZE: Final[int] = 100_000,
) -> Generator[float, None, None]:
    from sympy import primefactors

    pseudorand_num = generate_pseudorandom_numbers(
        seed=1,
        multiplier=6_364_136_223_846_793_005,
        increment=1_442_695_040_888_963_407,
        modulus=2**64,
        SAMPLE_SIZE=SAMPLE_SIZE,
    )
    number_of_all_cases: int = 0
    number_of_matches: int = 0
    for _ in SAMPLE_SIZE * ".":
        pseudrand_num: int = next(pseudorand_num)
        prime_divisors: List[int] = primefactors(pseudrand_num)
        if len(prime_divisors) < 2:
            continue
        first_prime_divisor: int = prime_divisors[-1]
        second_prime_divisor: int = prime_divisors[-2]
        number_of_all_cases += 1
        number_of_matches += int(second_prime_divisor**2 <= first_prime_divisor)
        if number_of_all_cases % 100 < 1:
            current_approx: float = number_of_matches / number_of_all_cases
            yield current_approx


def main(*args, **kwargs) -> None:
    logging.basicConfig(level=logging.INFO)
    _ = [
        logging.info(current_approx)
        for current_approx in approx_golomb_dickman_constant()
    ]


if __name__ == "__main__":
    main()
