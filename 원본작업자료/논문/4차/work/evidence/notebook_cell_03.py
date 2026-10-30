import subprocess, threading

GPU_LOG = []      # one dict per sample: time, used_mib, total_mib, util_pct, temp_c  (graph 9 of the final graph set)


class GpuSampler(threading.Thread):
    """Background thread: asks nvidia-smi every `every` seconds for as long as the kernel lives."""

    def __init__(self, every=15):
        super().__init__(daemon=True)
        self.every, self._halt = every, threading.Event()

    def run(self):
        while not self._halt.is_set():
            try:
                out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,memory.total,utilization.gpu,temperature.gpu",
                                      "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=5)
                if out.returncode == 0:
                    used, total, util, temp = [float(v) for v in out.stdout.strip().split("\n")[0].split(",")[:4]]
                    GPU_LOG.append(dict(time=time.time(), used_mib=used, total_mib=total, util_pct=util, temp_c=temp))
            except Exception:
                pass
            self._halt.wait(self.every)

    def stop(self):
        self._halt.set()


if "GPU_SAMPLER" in globals() and GPU_SAMPLER.is_alive():
    GPU_SAMPLER.stop()
GPU_SAMPLER = GpuSampler(every=15)
GPU_SAMPLER.start()
print("GPU sampler started (every 15 s; the timeline is graph 9 of Section 24)")