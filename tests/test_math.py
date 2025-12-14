"""Tests for math utilities."""

import unittest
from aoc.math import (
    count_continuous_segments,
    count_digits,
    calculate_toggle_states,
    gcd,
    lcm,
    lcm_multiple,
    gcd_multiple,
    is_prime,
    primes_up_to,
    prime_factors,
    mod_inverse,
    chinese_remainder_theorem,
)


class TestCountContinuousSegments(unittest.TestCase):
    """Tests for count_continuous_segments function."""

    def test_basic_segments(self):
        """Test counting continuous integer segments."""
        data = [0, 1, 2, 5, 6]
        self.assertEqual(count_continuous_segments(data), 2)  # [0,1,2] and [5,6]

    def test_single_segment(self):
        """Test single continuous segment."""
        data = [0, 1, 2, 3]
        self.assertEqual(count_continuous_segments(data), 1)

    def test_all_separate(self):
        """Test when all elements are separate."""
        data = [0, 2, 4, 6]
        self.assertEqual(count_continuous_segments(data), 4)

    def test_empty_list(self):
        """Test with empty list."""
        data = []
        self.assertEqual(count_continuous_segments(data), 0)

    def test_single_element(self):
        """Test with single element."""
        data = [1]
        self.assertEqual(count_continuous_segments(data), 1)

    def test_with_gaps(self):
        """Test with multiple gaps."""
        data = [1, 2, 3, 10, 11, 20]
        self.assertEqual(count_continuous_segments(data), 3)  # [1,2,3], [10,11], [20]


class TestCountDigits(unittest.TestCase):
    """Tests for count_digits function."""

    def test_single_digit(self):
        """Test counting digits in single digit number."""
        self.assertEqual(count_digits(5), 1)
        self.assertEqual(count_digits(0), 1)
        self.assertEqual(count_digits(9), 1)

    def test_multiple_digits(self):
        """Test counting digits in multiple digit numbers."""
        self.assertEqual(count_digits(12), 2)
        self.assertEqual(count_digits(123), 3)
        self.assertEqual(count_digits(12345), 5)

    def test_large_numbers(self):
        """Test counting digits in large numbers."""
        self.assertEqual(count_digits(1000000), 7)
        self.assertEqual(count_digits(999999999), 9)


class TestCalculateToggleStates(unittest.TestCase):
    """Tests for calculate_toggle_states function."""

    def test_basic_toggles(self):
        """Test basic toggle state calculation."""
        # Toggle indices: 0 twice, 1 once, 2 once
        toggles = [0, 1, 0, 2]
        states = calculate_toggle_states(toggles, 3)

        # Index 0: toggled 2 times (even) -> False
        # Index 1: toggled 1 time (odd) -> True
        # Index 2: toggled 1 time (odd) -> True
        self.assertEqual(states[0], False)
        self.assertEqual(states[1], True)
        self.assertEqual(states[2], True)

    def test_multiple_toggles(self):
        """Test with multiple toggles."""
        toggles = [1, 3, 2, 3]
        states = calculate_toggle_states(toggles, 5)

        # Index 0: not toggled -> False
        # Index 1: toggled 1 time (odd) -> True
        # Index 2: toggled 1 time (odd) -> True
        # Index 3: toggled 2 times (even) -> False
        # Index 4: not toggled -> False
        self.assertEqual(states[0], False)
        self.assertEqual(states[1], True)
        self.assertEqual(states[2], True)
        self.assertEqual(states[3], False)
        self.assertEqual(states[4], False)

    def test_no_toggles(self):
        """Test with no toggles."""
        toggles = []
        states = calculate_toggle_states(toggles, 3)

        self.assertEqual(states[0], False)
        self.assertEqual(states[1], False)
        self.assertEqual(states[2], False)

    def test_all_positions_toggled_once(self):
        """Test when all positions are toggled once."""
        toggles = [0, 1, 2]
        states = calculate_toggle_states(toggles, 3)

        self.assertEqual(states[0], True)
        self.assertEqual(states[1], True)
        self.assertEqual(states[2], True)

    def test_single_index_many_toggles(self):
        """Test single index toggled many times."""
        toggles = [0, 0, 0, 0, 0]  # 5 toggles (odd)
        states = calculate_toggle_states(toggles, 1)

        self.assertEqual(states[0], True)

    def test_even_toggles(self):
        """Test even number of toggles."""
        toggles = [0, 0, 0, 0]  # 4 toggles (even)
        states = calculate_toggle_states(toggles, 1)

        self.assertEqual(states[0], False)


class TestGCD(unittest.TestCase):
    """Tests for gcd function."""

    def test_basic_gcd(self):
        """Test basic GCD calculations."""
        self.assertEqual(gcd(12, 8), 4)
        self.assertEqual(gcd(17, 19), 1)
        self.assertEqual(gcd(100, 50), 50)

    def test_with_zero(self):
        """Test GCD with zero."""
        self.assertEqual(gcd(5, 0), 5)
        self.assertEqual(gcd(0, 5), 5)

    def test_identical_numbers(self):
        """Test GCD of identical numbers."""
        self.assertEqual(gcd(7, 7), 7)


class TestLCM(unittest.TestCase):
    """Tests for lcm function."""

    def test_basic_lcm(self):
        """Test basic LCM calculations."""
        self.assertEqual(lcm(12, 8), 24)
        self.assertEqual(lcm(3, 5), 15)
        self.assertEqual(lcm(10, 15), 30)

    def test_coprime_numbers(self):
        """Test LCM of coprime numbers."""
        self.assertEqual(lcm(7, 11), 77)

    def test_identical_numbers(self):
        """Test LCM of identical numbers."""
        self.assertEqual(lcm(5, 5), 5)


class TestLCMMultiple(unittest.TestCase):
    """Tests for lcm_multiple function."""

    def test_multiple_numbers(self):
        """Test LCM of multiple numbers."""
        self.assertEqual(lcm_multiple([2, 3, 4]), 12)
        self.assertEqual(lcm_multiple([5, 10, 15]), 30)

    def test_two_numbers(self):
        """Test LCM with two numbers."""
        self.assertEqual(lcm_multiple([6, 8]), 24)

    def test_many_numbers(self):
        """Test LCM with many numbers."""
        self.assertEqual(lcm_multiple([2, 3, 4, 5, 6]), 60)


class TestGCDMultiple(unittest.TestCase):
    """Tests for gcd_multiple function."""

    def test_multiple_numbers(self):
        """Test GCD of multiple numbers."""
        self.assertEqual(gcd_multiple([12, 18, 24]), 6)
        self.assertEqual(gcd_multiple([10, 15, 20]), 5)

    def test_coprime_numbers(self):
        """Test GCD of coprime numbers."""
        self.assertEqual(gcd_multiple([3, 5, 7]), 1)


class TestIsPrime(unittest.TestCase):
    """Tests for is_prime function."""

    def test_prime_numbers(self):
        """Test that prime numbers are identified correctly."""
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(3))
        self.assertTrue(is_prime(5))
        self.assertTrue(is_prime(17))
        self.assertTrue(is_prime(97))

    def test_non_prime_numbers(self):
        """Test that non-prime numbers are identified correctly."""
        self.assertFalse(is_prime(1))
        self.assertFalse(is_prime(4))
        self.assertFalse(is_prime(6))
        self.assertFalse(is_prime(100))

    def test_small_numbers(self):
        """Test edge cases with small numbers."""
        self.assertFalse(is_prime(0))
        self.assertFalse(is_prime(1))
        self.assertTrue(is_prime(2))


class TestPrimesUpTo(unittest.TestCase):
    """Tests for primes_up_to function."""

    def test_primes_up_to_10(self):
        """Test primes up to 10."""
        self.assertEqual(primes_up_to(10), [2, 3, 5, 7])

    def test_primes_up_to_20(self):
        """Test primes up to 20."""
        self.assertEqual(primes_up_to(20), [2, 3, 5, 7, 11, 13, 17, 19])

    def test_primes_up_to_1(self):
        """Test primes up to 1."""
        self.assertEqual(primes_up_to(1), [])

    def test_primes_up_to_2(self):
        """Test primes up to 2."""
        self.assertEqual(primes_up_to(2), [2])


class TestPrimeFactors(unittest.TestCase):
    """Tests for prime_factors function."""

    def test_simple_factorization(self):
        """Test simple prime factorizations."""
        self.assertEqual(prime_factors(12), {2: 2, 3: 1})
        self.assertEqual(prime_factors(100), {2: 2, 5: 2})

    def test_prime_number(self):
        """Test factorization of a prime number."""
        self.assertEqual(prime_factors(17), {17: 1})

    def test_power_of_prime(self):
        """Test factorization of a power of a prime."""
        self.assertEqual(prime_factors(8), {2: 3})
        self.assertEqual(prime_factors(27), {3: 3})

    def test_small_numbers(self):
        """Test factorization of small numbers."""
        self.assertEqual(prime_factors(1), {})
        self.assertEqual(prime_factors(2), {2: 1})


class TestModInverse(unittest.TestCase):
    """Tests for mod_inverse function."""

    def test_basic_mod_inverse(self):
        """Test basic modular inverse calculations."""
        self.assertEqual(mod_inverse(3, 11), 4)  # (3 * 4) % 11 == 1
        self.assertEqual(mod_inverse(10, 17), 12)  # (10 * 12) % 17 == 1

    def test_invalid_mod_inverse(self):
        """Test that ValueError is raised when inverse doesn't exist."""
        with self.assertRaises(ValueError):
            mod_inverse(2, 4)  # GCD(2, 4) = 2, not coprime


class TestChineseRemainderTheorem(unittest.TestCase):
    """Tests for chinese_remainder_theorem function."""

    def test_basic_crt(self):
        """Test basic Chinese Remainder Theorem."""
        # x ≡ 2 (mod 3), x ≡ 3 (mod 4), x ≡ 1 (mod 5)
        # Solution: x = 11
        result = chinese_remainder_theorem([2, 3, 1], [3, 4, 5])
        self.assertEqual(result, 11)

    def test_verify_solution(self):
        """Test that solution satisfies all congruences."""
        remainders = [2, 3, 1]
        moduli = [3, 4, 5]
        result = chinese_remainder_theorem(remainders, moduli)

        for remainder, modulus in zip(remainders, moduli):
            self.assertEqual(result % modulus, remainder)


if __name__ == '__main__':
    unittest.main()
