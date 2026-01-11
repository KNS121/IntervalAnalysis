import data_prep
import numpy as np
from plot import plot
import interval_functions

if __name__ == "__main__":
    x_data = data_prep.read_bin_files("-0.205_lvl_side_a_fast_data.bin")
    y_data = data_prep.read_bin_files("0.225_lvl_side_a_fast_data.bin")

    rad = 2 ** (-14)
    x_avg = data_prep.get_avg(x_data)
    y_avg = data_prep.get_avg(y_data)

    X = np.vectorize(data_prep.scalar_to_interval)(x_avg, rad).flatten()
    Y = np.vectorize(data_prep.scalar_to_interval)(y_avg, rad).flatten()

    bound_a_l = float(np.min(Y).a) - float(np.max(X).b)
    bound_a_r = float(np.max(Y).b) - float(np.min(X).a)

    bound_t_l = float(np.min(Y).a) / float(np.max(X).b)
    bound_t_r = float(np.max(Y).b) / float(np.min(X).a)

    number = 100
    eps_a = (bound_a_r - bound_a_l) / number
    eps_t = (bound_t_r - bound_t_l) / number

    print(f"\n a: [{bound_a_l:.4f}, {bound_a_r:.4f}], eps = {eps_a:.4f}")
    print(f"t: [{bound_t_l:.4f}, {bound_t_r:.4f}], eps = {eps_t:.4f}")

    plot("F1",
                    func_a=lambda a, X, Y: np.mean(interval_functions.jaccard_similarity(X + a, Y)),
                    func_t=lambda t, X, Y: np.mean(interval_functions.jaccard_similarity(X * t, Y)),
                    X=X, Y=Y,
                    bound_a_l=bound_a_l, bound_a_r=bound_a_r,
                    bound_t_l=bound_t_l, bound_t_r=bound_t_r
                    )

    plot("F2",
                    func_a=lambda a, X, Y: np.mean(interval_functions.jaccard_similarity(interval_functions.interval_mode(X + a), interval_functions.interval_mode(Y))),
                    func_t=lambda t, X, Y: np.mean(interval_functions.jaccard_similarity(interval_functions.interval_mode(X * t), interval_functions.interval_mode(Y))),
                    X=X, Y=Y,
                    bound_a_l=bound_a_l, bound_a_r=bound_a_r,
                    bound_t_l=bound_t_l, bound_t_r=bound_t_r
                    )

    plot("F3",
                    func_a=lambda a, X, Y: np.mean(interval_functions.jaccard_similarity(interval_functions.kreinovich(X + a), interval_functions.kreinovich(Y))),
                    func_t=lambda t, X, Y: np.mean(interval_functions.jaccard_similarity(interval_functions.kreinovich(X * t), interval_functions.kreinovich(Y))),
                    X=X, Y=Y,
                    bound_a_l=bound_a_l, bound_a_r=bound_a_r,
                    bound_t_l=bound_t_l, bound_t_r=bound_t_r
                    )

    plot("F4",
                    func_a=lambda a, X, Y: np.mean(
                        interval_functions.jaccard_similarity(interval_functions.prolubnikov(X + a), interval_functions.prolubnikov(Y))),
                    func_t=lambda t, X, Y: np.mean(
                        interval_functions.jaccard_similarity(interval_functions.prolubnikov(X * t), interval_functions.prolubnikov(Y))),
                    X=X, Y=Y,
                    bound_a_l=bound_a_l, bound_a_r=bound_a_r,
                    bound_t_l=bound_t_l, bound_t_r=bound_t_r
                    )

