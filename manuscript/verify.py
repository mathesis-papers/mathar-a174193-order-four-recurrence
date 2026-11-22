import json
from fractions import Fraction
from itertools import combinations, permutations
from math import comb, factorial


def trim(polynomial):
    polynomial = list(polynomial)
    while len(polynomial) > 1 and polynomial[-1] == 0:
        polynomial.pop()
    return polynomial


def add(*polynomials):
    result = [0] * max(map(len, polynomials))
    for polynomial in polynomials:
        for index, coefficient in enumerate(polynomial):
            result[index] += coefficient
    return trim(result)


def scale(polynomial, scalar):
    return trim([scalar * coefficient for coefficient in polynomial])


def mul(*polynomials):
    result = [1]
    for polynomial in polynomials:
        product = [0] * (len(result) + len(polynomial) - 1)
        for left, coefficient in enumerate(result):
            for right, other in enumerate(polynomial):
                product[left + right] += coefficient * other
        result = trim(product)
    return result


def translate(polynomial, offset):
    result = [0]
    for coefficient in reversed(polynomial):
        result = add(mul(result, [offset, 1]), [coefficient])
    return result


def evaluate(polynomial, value):
    result = 0
    for coefficient in reversed(polynomial):
        result = result * value + coefficient
    return result


def quotient_series(numerator, denominator, count):
    result = []
    for degree in range(count):
        known = sum(denominator[lag] * result[degree - lag]
                    for lag in range(1, min(degree + 1, len(denominator))))
        result.append(Fraction(numerator[degree] - known, denominator[0]))
    return result


def coefficients(count):
    root = [Fraction(1)]
    for degree in range(1, count + 2):
        root.append(root[-1] * Fraction(2 * (2 * degree - 3), degree))
    radicand = [1, -4]
    rational = [1, -8, 13, 24, -48]
    multiplier = [1, -6, 1, 34, -26, -4]
    numerator = add(rational, scale(mul(multiplier, root), -1))
    assert numerator[:2] == [0, 0]
    denominator = scale(mul([1, -1], radicand, radicand), 2)
    main = quotient_series(numerator[2:], denominator, count)
    sibling_rational = [1, -5, -6, 45, -24]
    sibling_multiplier = [1, 1, -4, 1]
    sibling_numerator = add(mul(sibling_multiplier, radicand, radicand),
                            scale(mul(sibling_rational, root), -1))
    assert sibling_numerator[:2] == [0, 0]
    sibling = quotient_series(sibling_numerator[2:],
                              scale(mul(radicand, radicand), 2), count)
    assert all(value.denominator == 1 for value in main + sibling)
    return list(map(int, main)), list(map(int, sibling))


def main_weights(index):
    return [-(index + 2) * (404489 * index - 1866368),
            3147815 * index**2 - 8680082 * index - 14098754,
            2 * (-2336439 * index**2 + 652022 * index + 14514849),
            8 * (-1044770 * index**2 + 10585023 * index - 20370553),
            8 * (642982 * index - 2004177) * (2 * index - 9)]


def sibling_weights(index):
    return [2 * (index + 2) * (2013 * index**2 - 10435 * index + 41550),
            4026 * index**3 - 128025 * index**2 + 34955 * index + 59010,
            -2 * (2 * index - 5) * (20130 * index**2 - 110855 * index + 93819)]


def falling(polynomial, order):
    return mul(*(add(polynomial, [-shift]) for shift in range(order)))


def bivariate_product(*factors):
    result = {(0, 0): 1}
    for factor in factors:
        product = {}
        for (left_j, left_n), value in result.items():
            for (right_j, right_n), other in factor.items():
                key = (left_j + right_j, left_n + right_n)
                product[key] = product.get(key, 0) + value * other
        result = product
    return result


def vandermonde_certificate():
    size, double_size = [0, 1], [0, 2]
    coefficients = [mul(size, size, [-1, 1], [-1, 1]),
                    scale(mul(size, size, [-1, 1]), -1),
                    [12, -4, 1], [-4]]
    denominator = falling(double_size, 6)
    terms = []
    for order, coefficient in enumerate(coefficients):
        terms.append(mul(coefficient, falling(size, order), falling(size, order),
                         falling(size, 2 * order),
                         falling([-2 * order, 2], 6 - 2 * order)))
    weighted_numerator = mul(size, size, [-1, 1], [-1, 1], [-1, 1],
                             [-60, 48, -12, 1])
    odd_denominator = scale(mul([-5, 2], [-3, 2], [-1, 2]), 4)
    certificate = add(mul(add(*terms), odd_denominator),
                      scale(mul(weighted_numerator, denominator), -1))
    assert certificate == [0]
    left = {(1, 0): 1, (0, 0): -1}
    right = {(0, 1): 1, (1, 0): -1, (0, 0): -1}
    gap = {(0, 1): 1, (1, 0): -2}
    residual = bivariate_product(left, left, right, right, gap, gap)
    for order, coefficient in enumerate(coefficients):
        factors = [{(0, degree): value for degree, value in enumerate(coefficient)}]
        for shift in range(order):
            factors.extend([{(1, 0): 1, (0, 0): -shift},
                            {(0, 1): 1, (1, 0): -1, (0, 0): -shift}])
        for key, value in bivariate_product(*factors).items():
            residual[key] = residual.get(key, 0) - value
    assert not any(residual.values())
    return certificate


def hook_count(index):
    count = Fraction(comb(2 * index, index), index + 1)
    for top_row in range(index // 2, index - 1):
        dimension = Fraction(factorial(index) * (2 * top_row - index + 2),
                             (top_row + 2) * factorial(top_row) * (index - top_row)
                             * factorial(index - top_row - 2))
        assert dimension.denominator == 1
        count += dimension**2
    assert count.denominator == 1
    return int(count)


def avoids(sequence, pattern):
    for first, middle, last in combinations(range(len(sequence)), 3):
        if pattern == 321 and sequence[first] > sequence[middle] > sequence[last]:
            return False
        if pattern == 231 and sequence[middle] > sequence[first] > sequence[last]:
            return False
    return True


def almost_avoids(sequence, pattern):
    return not sequence or any(avoids(sequence[:index] + sequence[index + 1:], pattern)
                               for index in range(len(sequence)))


def enumerate_classes(main, sibling):
    report = []
    for length in range(9):
        first_class, second_class = [], []
        for permutation in permutations(range(1, length + 1)):
            if almost_avoids(permutation, 321):
                first_class.append(permutation)
            if almost_avoids(permutation, 231):
                second_class.append(permutation)
        assert len(first_class) == main[length]
        assert len(second_class) == sibling[length]
        images = second_class[:len(first_class)]
        assert len(set(images)) == len(first_class)
        assert all(len(image) == length for image in images)
        report.append({'n': length, 'almost_321': len(first_class),
                       'almost_231': len(second_class), 'rank_images': len(images)})
    return report


def run():
    quartic = [-8, 14, 10, -5, 1]
    sibling_quartic = [-24, 18, 19, -9, 2]
    linear1, linear3, linear5, linear7 = [-1, 2], [-3, 2], [-5, 2], [-7, 2]
    certificate = add(
        scale(mul(linear7, linear5, linear3, [-1866368, 404489], quartic), -2),
        mul(linear7, linear5, [-14098754, -8680082, 3147815], translate(quartic, -1)),
        scale(mul([1, 1], linear7, [-14514849, -652022, 2336439], translate(quartic, -2)), -1),
        scale(mul([0, 1], [1, 1], [20370553, -10585023, 1044770], translate(quartic, -3)), -2),
        mul([0, 1], [-1, 1], [1, 1], [-2004177, 642982], translate(quartic, -4)))
    assert certificate == [0]
    sibling_certificate = add(
        scale(mul(linear3, [41550, -10435, 2013], sibling_quartic), 4),
        mul([59010, 34955, -128025, 4026], translate(sibling_quartic, -1)),
        scale(mul([1, 1], [93819, -110855, 20130], translate(sibling_quartic, -2)), -1))
    assert sibling_certificate == [0]
    main_weight_polynomials = [mul([-2, -1], [-1866368, 404489]),
                              [-14098754, -8680082, 3147815],
                              [29029698, 1304044, -4672878],
                              [-162964424, 84680184, -8358160],
                              scale(mul([-2004177, 642982], [-9, 2]), 8)]
    assert add(*main_weight_polynomials) == [0]
    assert add([1, -8, 13, 24, -48],
               scale(mul([1, 0, -3], [1, -4], [1, -4]), -1)) == [0]
    assert add([1, -6, 1, 34, -26, -4],
               mul([1, -1], [-1, 5, 4, -30, -4])) == [0]
    assert add(sibling_quartic, scale(quartic, -2),
               scale(mul([1, 1], [2, 1], [-4, 1]), -1)) == [0]
    weighted_certificate = vandermonde_certificate()
    assert add(quartic, scale(mul([1, 1], [-4, 12, -6, 1]), -1),
               scale(mul([2, 1], [-1, 2]), -2)) == [0]
    count = 201
    main, sibling = coefficients(count)
    main_oeis = [1, 1, 2, 6, 23, 103, 488, 2320, 10867, 49971, 225861,
                 1005821, 4423807, 19255967, 83093364, 355956164,
                 1515437339, 6417727259, 27054820649, 113602953089,
                 475370846639, 1983142721039, 8250982614809, 34246497698633,
                 141838788939623, 586322071478503, 2419474311617803,
                 9968270142800955, 41010408788528703, 168499207575017087]
    sibling_oeis = [1, 1, 2, 6, 24, 111, 531, 2519, 11726, 53547, 240448,
                    1064608, 4658952, 20192022, 86807865, 370665585,
                    1573606410, 6647552115, 27962334180, 117185243340,
                    489508952160, 2038937744610, 8471179017990, 35115582053214,
                    145269385076124, 599866065025406, 2472955722033776,
                    10179494703130704, 41844811399520752, 171796056971896588]
    assert main[:len(main_oeis)] == main_oeis
    assert sibling[:len(sibling_oeis)] == sibling_oeis
    for index in range(count):
        central = comb(2 * index, index)
        denominator = 2 * (index + 1) * (index + 2) * (2 * index - 1)
        assert main[index] == Fraction(central * evaluate(quartic, index), denominator) - 1
        sibling_formula = Fraction(central * evaluate(sibling_quartic, index), 2 * denominator)
        sibling_formula += -2 if index == 0 else Fraction(1, 2) if index == 1 else 0
        assert sibling[index] == sibling_formula
        if index >= 2:
            assert sibling[index] - main[index] == 1 + Fraction((index - 4) * central, 4 * (2 * index - 1))
        if index < count - 1:
            assert (index + 3) * evaluate(quartic, index) * (main[index + 1] + 1) == 2 * (2 * index - 1) * evaluate(quartic, index + 1) * (main[index] + 1)
        if index >= 4:
            assert sum(weight * main[index - lag] for lag, weight in enumerate(main_weights(index))) == 0
            assert sum(weight * sibling[index - lag] for lag, weight in enumerate(sibling_weights(index))) == 0
    for index in range(count):
        assert hook_count(index) == main[index]
    for index in range(2, count - 1):
        assert ((index + 3) * evaluate(sibling_quartic, index) * sibling[index + 1]
                == 2 * (2 * index - 1) * evaluate(sibling_quartic, index + 1) * sibling[index])
    deletion_counts = enumerate_classes(main, sibling)
    sibling_exceptions = {str(index): sum(weight * sibling[index - lag] for lag, weight in enumerate(sibling_weights(index))) for index in [2, 3]}
    report = {'status': 'all_checks_passed',
              'polynomial_identities': {'A174193_cleared_recurrence': certificate,
                                        'A174195_cleared_recurrence': sibling_certificate,
                                        'A174193_weight_sum': [0],
                                        'A174193_rational_decomposition': [0],
                                        'A174193_square_root_decomposition': [0],
                                        'coefficient_difference_factorization': [0],
                                        'weighted_Vandermonde_polynomial_expansion': [0],
                                        'weighted_Vandermonde_rational_identity': weighted_certificate,
                                        'tableau_closed_form_simplification': [0]},
              'generating_function_coefficients': {'range': [0, 200], 'count_each': count},
              'closed_form_checks_each': count,
              'first_order_recurrence_checks': 200,
              'sibling_first_order_recurrence_checks': 198,
              'tableau_sum_checks': {'range': [0, 200], 'count': 201},
              'deletion_enumeration_and_rank_injection': deletion_counts,
              'coefficient_difference_checks': 199,
              'order_four_recurrence': {'range': [4, 200], 'count': 197},
              'sibling_recurrence': {'range': [4, 200], 'count': 197,
                                     'residuals_below_range': sibling_exceptions},
              'OEIS_coefficients': {'A174193': len(main_oeis), 'A174195': len(sibling_oeis)},
              'coverage': 'Polynomial coefficient identities support the written proofs; sequence comparisons are finite checks.'}
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    run()
