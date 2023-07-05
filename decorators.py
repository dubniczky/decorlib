import time
import tracemalloc
from functools import wraps

todo_counter = 0


def placeholder(func):
    '''
    This is a placeholder decorator, it does nothing.
    Returns the result of the called function.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def performance(func):
    '''
    Measures time and maximum memory usage of the decorated function.
    Returns the result of the called function.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        tracemalloc.start()
        
        result = func(*args, **kwargs)
        
        _, peak = tracemalloc.get_traced_memory()
        end_time = time.perf_counter()
        print(f'{func.__name__}(): {(end_time-start_time):.3f} s, {peak/10**6:.3f} Mb')
        tracemalloc.stop()
        return result
    return wrapper


def todo(func):
    '''
    Prints alerts for functions marked as todo
    Returns the result of the called function.
    '''
    global todo_counter
    todo_counter += 1
    print(f'{todo_counter}. TODO {func.__name__}()')
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f'ALERT: TODO function called {func.__name__}()')
        return func(*args, **kwargs)
    return wrapper


def repeat(count : int = 1, delay : float = None):
    '''
    Creates a decorator that runs the function `count` times, with any seconds of delay. If the `delay` is set to `None`, the sleep method is not called to prevent context switching in the background.
    Returns a list of the returned values from the function calls.
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if delay is None:
                return [func(*args, **kwargs) for _ in range(count)]
            
            result = []
            for _ in range(count):
                result.append(func(*args, **kwargs))
                time.sleep(delay)
            return result
        return wrapper
    return decorator


def retry(count : int = 3, *, exception : Exception = Exception, delay : float = None, log : bool = True):
    '''
    Decorator that retries the execution of a function if it raises a specific exception.
    Returns the result of the called function, or raises an exception if all retries fail.
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            exc = None
            for i in range(1, count+1):
                try:
                    return func(*args, **kwargs)
                except exception as e:
                    exc = e
                    if log:
                        print(f"{func.__name__}() raised {e.__class__.__name__}.", end='')
                        if delay is None:
                            print(f"Retry {i}...")
                        else:
                            print(f"Retry {i} in: {delay} seconds")
                        
                    if i < count and delay is not None:
                        time.sleep(delay)
            raise exc
        return wrapper
    return decorator


def ignore(exception : Exception = Exception, default = None):
    '''
    Decorator that ignores all or specific exceptions that .
    Returns the result of the called function, or the default value if it raised an exception.
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception:
                return default
        return wrapper
    return decorator

def limit_frequency(time_limit : float = 1.0, *, default = None, return_last : bool = False):
    '''
    Limits the execution frequency of the function to a certain time.
    Returns the result of the called function, or the last value if it's enabled, default value if it's disabled
    '''
    last_value = default
    last_called = None
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_value, last_called
            now = time.time()
            if last_called is None:
                last_called = now
            elif now - last_called < time_limit:
                if return_last:
                    return last_value
                else:
                    return default
            
            try:
                last_value = func(*args, **kwargs)
                return last_value
            finally:
                last_called = now
            
        return wrapper
    return decorator



@limit_frequency()
def asd(a):
    print(a)
    return a
    
print(asd('1'))
print(asd('2'))
print(asd('3'))