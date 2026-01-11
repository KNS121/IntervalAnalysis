#include <vector>
#include <algorithm>
#include <set>
#include <iostream>

#ifdef _WIN32
#define DLL_EXPORT __declspec(dllexport)
#else
#define DLL_EXPORT
#endif

extern "C" {

    struct Interval {
        double a;
        double b;
    };

    struct IntervalArray {
        Interval* intervals;
        int count;
    };

    DLL_EXPORT bool interval_intersection(const Interval& x, const Interval& y) {
        return !(x.b < y.a || y.b < x.a);
    }

    DLL_EXPORT Interval interval_union(const Interval& x, const Interval& y) {
        Interval result;
        result.a = std::min(x.a, y.a);
        result.b = std::max(x.b, y.b);
        return result;
    }

    // Функция, которая возвращает указатель на выделенную память
    DLL_EXPORT IntervalArray* interval_moda_cpp(
        const double* a_arr,
        const double* b_arr,
        int n
    ) {
        std::vector<Interval> intervals;
        for (int i = 0; i < n; i++) {
            intervals.push_back({ a_arr[i], b_arr[i] });
        }

        std::set<double> boundaries;
        for (const auto& interval : intervals) {
            boundaries.insert(interval.a);
            boundaries.insert(interval.b);
        }

        std::vector<double> sorted_boundaries(boundaries.begin(), boundaries.end());
        std::sort(sorted_boundaries.begin(), sorted_boundaries.end());

        std::vector<Interval> elementary_intervals;
        for (size_t i = 0; i < sorted_boundaries.size() - 1; i++) {
            elementary_intervals.push_back({ sorted_boundaries[i], sorted_boundaries[i + 1] });
        }

        std::vector<int> intersection_counts(elementary_intervals.size(), 0);
        for (size_t i = 0; i < elementary_intervals.size(); i++) {
            for (const auto& interval : intervals) {
                if (interval_intersection(elementary_intervals[i], interval)) {
                    intersection_counts[i]++;
                }
            }
        }

        int max_count = 0;
        for (int count : intersection_counts) {
            if (count > max_count) max_count = count;
        }

        std::vector<Interval> modal_elementary_intervals;
        for (size_t i = 0; i < elementary_intervals.size(); i++) {
            if (intersection_counts[i] == max_count) {
                modal_elementary_intervals.push_back(elementary_intervals[i]);
            }
        }

        std::vector<Interval> merged_intervals;
        if (!modal_elementary_intervals.empty()) {
            Interval current_interval = modal_elementary_intervals[0];

            for (size_t i = 1; i < modal_elementary_intervals.size(); i++) {
                Interval next_interval = modal_elementary_intervals[i];
                if (interval_intersection(current_interval, next_interval)) {
                    current_interval = interval_union(current_interval, next_interval);
                }
                else {
                    merged_intervals.push_back(current_interval);
                    current_interval = next_interval;
                }
            }
            merged_intervals.push_back(current_interval);
        }

        // Выделение памяти для результата
        IntervalArray* result = new IntervalArray;
        result->count = static_cast<int>(merged_intervals.size());
        result->intervals = new Interval[result->count];

        for (int i = 0; i < result->count; i++) {
            result->intervals[i] = merged_intervals[i];
        }

        return result;
    }

    // Функция для освобождения памяти
    DLL_EXPORT void free_interval_array(IntervalArray* arr) {
        if (arr) {
            delete[] arr->intervals;
            delete arr;
        }
    }
}