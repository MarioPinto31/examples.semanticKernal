# Semantic Kernel Dev UI and Observability in Python

## 🧩 Short answer
👉 **Yes — it can work with a Semantic Kernel app in Python**, **but only if** you initialize and instrument the kernel with the right configuration.  
However, the Dev UI is mainly meant for **local development and debugging**, not production, and it’s **not automatically aware of your app** unless you expose the right hooks.

---

## ⚙️ How it works
The **Semantic Kernel Dev UI** is a small **local web dashboard** that connects to a running **Kernel instance**.  
It can visualize:
- Function graphs  
- Context variables  
- Prompt templates  
- Execution logs  

It doesn’t “hook” into your app automatically — you must:
1. Install the Dev UI package  
2. Initialize it with your `Kernel` instance  
3. Run your SK app with the Dev UI server running  

---

## 🧱 Installation

```bash
pip install semantic-kernel[dev]
```

---

## 🧠 Example Integration

Here’s a minimal pattern that makes it work inside your Semantic Kernel Python app:

```python
from semantic_kernel import Kernel
from semantic_kernel.dev import DevKernelServer

# 1️⃣ Create your SK kernel as usual
kernel = Kernel()

# 2️⃣ Wrap your kernel with the Dev UI server
dev_ui = DevKernelServer(kernel)

# 3️⃣ Run your app (the Dev UI will be accessible in the browser)
dev_ui.run(port=5050)  # default http://localhost:5050
```

Now, when you open `http://localhost:5050`, you’ll see a dashboard where you can:
- Inspect the available skills/plugins
- See logs of invocations
- Visualize prompts and responses

---

## 🔄 Integrating with your app

If you already have your own main loop or async app (like FastAPI, Streamlit, etc.), you can **run the Dev UI server in a background thread**:

```python
import threading

def start_dev_ui(kernel):
    from semantic_kernel.dev import DevKernelServer
    DevKernelServer(kernel).run(port=5050)

threading.Thread(target=start_dev_ui, args=(kernel,), daemon=True).start()
```

That way, the Dev UI runs alongside your existing app and observes kernel activity.

---

## 🚫 Current limitations (as of late 2025)

| Feature | Status |
|----------|--------|
| Works with async kernel execution | ✅ Yes |
| Automatically detects all functions | ✅ Mostly, if added via `kernel.add_plugin` |
| Tracks execution context | ✅ Partially |
| Production-safe | ❌ No — it’s a local debug tool |
| Remote deployment | ❌ Not supported (local only) |

So:  
- ✅ Great for **developing or debugging** a Semantic Kernel pipeline  
- 🚫 Not for production monitoring or observability  
  (for that, you’d use Prometheus/Grafana/OpenTelemetry)

---

## 🧭 Recommended pattern

If you want a **full development + observability** experience:
- Use **Dev UI** locally during prompt and plugin development  
- Use **Prometheus + Grafana** and/or **OpenTelemetry** in staging or production  
