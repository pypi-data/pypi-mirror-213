import os
import sys
import pdb
import inspect
import builtins
from functools import wraps


def __zhijxu_is_rank_0():
    if os.environ.get("LOCAL_RANK", "0") == "0":
        return True
    return False


def zhijxu_run_once(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return func(*args, **kwargs)

    wrapper.has_run = False
    return wrapper


@zhijxu_run_once
def zhijxu_vscode_attach(sleep_time_sec=3):
    """
    only rank 0 will wait for vscode debug attach, other rank continue to run
    """
    import debugpy
    from termcolor import cprint
    import time as tmp_time

    if __zhijxu_is_rank_0():
        debugpy.listen(("localhost", 56789))
        tmp_time.sleep(
            sleep_time_sec
        )  # so the next print can be shown at last line of terminal in multiprocess case
        cprint("\n\nzhijxu, waiting for debug connect\n\n", color="red", flush=True)
        debugpy.wait_for_client()
        cprint("\n\nzhijxu,debug connection done!!!\n\n", color="red", flush=True)


def zhijxu_do_bench(
    fn,
    warmup=25,
    rep=100,
    grad_to_none=None,
    percentiles=(0.5, 0.2, 0.8),
    fast_flush=False,
):
    """
    example call: do_bench(lambda: matmul(a,b))

    Benchmark the runtime of the provided function. By default, return the median runtime of :code:`fn` along with
    the 20-th and 80-th performance percentile.

    :param fn: Function to benchmark
    :type fn: Callable
    :param warmup: Warmup time (in ms)
    :type warmup: int
    :param rep: Repetition time (in ms)
    :type rep: int
    :param grad_to_none: Reset the gradient of the provided tensor to None
    :type grad_to_none: torch.tensor, optional
    :param percentiles: Performance percentile to return in addition to the median.
    :type percentiles: list[float]
    :param fast_flush: Use faster kernel to flush L2 between measurements
    :type fast_flush: bool
    """
    import torch

    # Estimate the runtime of the function
    fn()
    torch.cuda.synchronize()
    start_event = torch.cuda.Event(enable_timing=True)
    end_event = torch.cuda.Event(enable_timing=True)
    start_event.record()
    for _ in range(5):
        fn()
    end_event.record()
    torch.cuda.synchronize()
    estimate_ms = start_event.elapsed_time(end_event) / 5
    # compute number of warmup and repeat
    n_warmup = max(1, int(warmup / estimate_ms))
    n_repeat = max(1, int(rep / estimate_ms))
    # We maintain a buffer of 256 MB that we clear
    # before each kernel call to make sure that the L2
    # doesn't contain any input data before the run
    start_event = [torch.cuda.Event(enable_timing=True) for i in range(n_repeat)]
    end_event = [torch.cuda.Event(enable_timing=True) for i in range(n_repeat)]
    if fast_flush:
        cache = torch.empty(int(256e6 // 4), dtype=torch.int, device="cuda")
    else:
        cache = torch.empty(int(256e6), dtype=torch.int8, device="cuda")
    # Warm-up
    for _ in range(n_warmup):
        fn()
    # Benchmark
    for i in range(n_repeat):
        # we don't want `fn` to accumulate gradient values
        # if it contains a backward pass. So we clear the
        # provided gradients
        if grad_to_none is not None:
            for x in grad_to_none:
                x.grad = None
        # we clear the L2 cache before each run
        cache.zero_()
        # record time of `fn`
        start_event[i].record()
        fn()
        end_event[i].record()
    # Record clocks
    torch.cuda.synchronize()
    times = torch.tensor([s.elapsed_time(e) for s, e in zip(start_event, end_event)])
    if percentiles:
        percentiles = torch.quantile(times, torch.tensor(percentiles)).tolist()
        return tuple(percentiles)
    else:
        return torch.mean(times).item()


def zhijxu_cuda_profiling(step):
    """
    the control env and its possible values are:
        - VIZTRACER, 0/1
        - NSYS, 0/1
        - START_STEP, any integer larger than 0
        - END_STEP, any integer larger than START_STEP
    """
    from termcolor import cprint
    import torch
    from viztracer import VizTracer

    if os.environ.get("VIZTRACER", "0") == "1":
        assert (
            os.environ["CUDA_LAUNCH_BLOCKING"] == "1"
        ), "CUDA_LAUNCH_BLOCKING must be set to 1 when using VizTracer to profile CUDA code"
        if step == 0:
            tracer = VizTracer(output_file=f"trace_{os.getpid()}.json")
        if step == int(os.environ.get("START_STEP", 10)):
            cprint("Start tracing", "red")
            tracer.start()
        if step == int(os.environ.get("END_STEP", 20)):
            cprint("Stop tracing", "red")
            tracer.stop()
            tracer.save()
            sys.exit(0)
    if os.environ.get("NSYS", "0") == "1":
        assert (
            os.environ.get("CUDA_LAUNCH_BLOCKING", "0") != "1"
        ), "CUDA_LAUNCH_BLOCKING must not be set to 1 when using nsys"
        if step == int(os.environ.get("START_STEP", 10)):
            cprint("Start tracing", "red")
            torch.cuda.cudart().cudaProfilerStart()
        if step == int(os.environ.get("END_STEP", 20)):
            cprint("Stop tracing", "red")
            torch.cuda.cudart().cudaProfilerStop()


@zhijxu_run_once
def zhijxu_pdb():
    """
        only rank 0 will enter pdb, other ranks continue execution
    """
    if __zhijxu_is_rank_0():
        from termcolor import cprint

        cprint("zhijxu, i am rank 0, enter pdb now", "red")
        pdb.set_trace()


@zhijxu_run_once
def zhijxu_enter_pdb_at_exception():
    """
        register a hook which will enter pdb when process wants to exit, this will help debugging when process has un-caught exception
    """
    import atexit

    atexit.register(pdb.pm)


def zhijxu_open_onnx_in_tensorboard(model, port):
    """
    give the onnx model path and tensorboard port, then will convert to tensorboard and launch tensorboard automatically for you
    """
    from tempfile import mkdtemp
    tmp_dir = mkdtemp(prefix="onnx-tensorboard-")
    from termcolor import cprint
    cprint(f"converted tensorboard is put at {tmp_dir}", "red")
    os.system(f"python /home/zhijxu/onnxruntime/tools/python/onnx2tfevents.py --logdir={tmp_dir} --model {model}")
    os.system(f"tensorboard --logdir={tmp_dir} --port {port} &")


def xr_log(func):
    import logging
    # configure logging format and level
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    # define the wrapper function
    def wrapper(*args, **kwargs):
        # log before calling the original function
        logging.info(f"xr Running {func.__name__} with arguments {args} and {kwargs}")
        # call the original function and store its result
        result = func(*args, **kwargs)
        # log after calling the original function
        logging.info(f"xr Finished {func.__name__} with result {result}")
        # return the result of the original function
        return result
    # return the wrapper function
    return wrapper

def xr_timer(func):
    import time
    # define the wrapper function
    def wrapper(*args, **kwargs):
        # record the start time
        start = time.perf_counter()
        # call the original function
        result = func(*args, **kwargs)
        # record the end time
        end = time.perf_counter()
        # calculate the elapsed time
        duration = end - start
        # print the elapsed time
        print(f"xr found {func.__name__} took {duration:.4f} seconds")
        # return the result of the original function
        return result
    # return the wrapper function
    return wrapper

fset = {
    name: obj
    for name, obj in inspect.getmembers(sys.modules[__name__])
    if inspect.isfunction(obj) and name.startswith(("zhijxu_","xr_"))
}
for name, obj in fset.items():
    if inspect.isfunction(obj):
        setattr(builtins, name, obj)

