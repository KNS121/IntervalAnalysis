import numpy as np
import intvalpy as ip

_interval_moda_available = False
_interval_moda_func = None

try:
    import ctypes
    from ctypes import c_double, c_int, POINTER, Structure

    class _Interval(ctypes.Structure):
        _fields_ = [("a", c_double), ("b", c_double)]

    class _IntervalArray(ctypes.Structure):
        _fields_ = [("intervals", POINTER(_Interval)), ("count", c_int)]

    try:
        lib = ctypes.CDLL('./interval_moda.dll')
    except OSError:
        lib = ctypes.CDLL('interval_moda.dll')

    lib.interval_moda_cpp.argtypes = [
        POINTER(c_double),  # a_arr
        POINTER(c_double),  # b_arr
        c_int               # n
    ]
    lib.interval_moda_cpp.restype = POINTER(_IntervalArray)

    lib.free_interval_array.argtypes = [POINTER(_IntervalArray)]
    lib.free_interval_array.restype = None

    def _call_interval_moda_cpp(intervals):
        if not intervals:
            return []
        a_arr = np.array([float(iv.a) for iv in intervals], dtype=np.float64)
        b_arr = np.array([float(iv.b) for iv in intervals], dtype=np.float64)
        n = len(a_arr)

        a_ptr = a_arr.ctypes.data_as(POINTER(c_double))
        b_ptr = b_arr.ctypes.data_as(POINTER(c_double))

        result_ptr = lib.interval_moda_cpp(a_ptr, b_ptr, n)
        if not result_ptr:
            return []

        result = result_ptr.contents
        output = []
        for i in range(result.count):
            iv = result.intervals[i]
            output.append(ip.Interval([iv.a, iv.b]))

        lib.free_interval_array(result_ptr)
        return output

    _interval_moda_func = _call_interval_moda_cpp
    _interval_moda_available = True
    print("DLL 'interval_moda.dll' успешно загружена. Используется C++ реализация моды.")

except Exception as e:
    print(f"Не удалось загрузить interval_moda.dll: {e}")



def interval_mode(intervals):
    if isinstance(intervals, np.ndarray):
        intervals = intervals.tolist()
    if not intervals:
        return []

    if _interval_moda_available and _interval_moda_func is not None:
        try:
            return _interval_moda_func(intervals)
        except Exception as e:
            print(f"Ошибка при вызове DLL: {e}. Переключение на Python-реализацию.")