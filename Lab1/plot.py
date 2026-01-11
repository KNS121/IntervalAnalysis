import matplotlib.pyplot as plt
import numpy as np
from interval_functions import golden_search

def plot(name, func_a, func_t, X, Y,
                    bound_a_l, bound_a_r, bound_t_l, bound_t_r, eps=1e-3):

    # --- Оптимизация методом золотого сечения ---
    a_opt_gs = golden_search(lambda a: func_a(a, X, Y), bound_a_l, bound_a_r, eps)
    t_opt_gs = golden_search(lambda t: func_t(t, X, Y), bound_t_l, bound_t_r, eps)
    val_a_gs = func_a(a_opt_gs, X, Y)
    val_t_gs = func_t(t_opt_gs, X, Y)
    print("Gold_search:")
    print(f"{name}: a* = {a_opt_gs:.4f} (F={val_a_gs:.4f}), t* = {t_opt_gs:.4f} (F={val_t_gs:.4f})")

    # --- Построение дискретных графиков ---
    a_values = np.linspace(bound_a_l, bound_a_r, 100)
    t_values = np.linspace(bound_t_l, bound_t_r, 100)

    # --- Вычисление значений функционалов ---
    Ji_a = [func_a(a, X, Y) for a in a_values]
    Ji_t = [func_t(t, X, Y) for t in t_values]

    # --- Поиск максимумов по дискретным значениям ---
    idx_a_max = np.argmax(Ji_a)
    idx_t_max = np.argmax(Ji_t)
    a_opt, val_a = a_values[idx_a_max], Ji_a[idx_a_max]
    t_opt, val_t = t_values[idx_t_max], Ji_t[idx_t_max]

    print("Real:")
    print(f"{name}: a* = {a_opt:.4f} (F={val_a:.4f}), t* = {t_opt:.4f} (F={val_t:.4f})")

    # --- Первый график: F(a) ---
    plt.figure(figsize=(8, 6))
    plt.plot(a_values, Ji_a, label=f"{name}(a)", color="black")
    plt.scatter(a_opt, val_a, color='red', s=100, zorder=5, label=f"a* = {a_opt:.4f}")
    plt.title(f"{name}(a)")
    plt.xlabel("a")
    plt.ylabel("Jaccard")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"pictures/{name}_a.png", dpi=300)
    plt.close()

    # --- Второй график: F(t) ---
    plt.figure(figsize=(8, 6))
    plt.plot(t_values, Ji_t, label=f"{name}(t)", color="blue")
    plt.scatter(t_opt, val_t, color='red', s=100, zorder=5, label=f"t* = {t_opt:.4f}")
    plt.title(f"{name}(t)")
    plt.xlabel("t")
    plt.ylabel("Jaccard")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"pictures/{name}_t.png", dpi=300)
    plt.close()