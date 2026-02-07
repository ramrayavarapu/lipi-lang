// Pyodide-based Lipi-Lang Runtime for Browser Execution
// Loads CPython via WebAssembly (Pyodide) and runs the real lipi.py interpreter

const LipiPyodide = (() => {
    let pyodide = null;
    let isLoading = false;
    let isReady = false;
    let onReadyCallbacks = [];
    let useFallbackInterpreter = false;

    // The lipi.py interpreter source will be fetched and stored here
    let lipiInterpreterSource = null;

    /**
     * Initialize Pyodide and load the lipi.py interpreter.
     * Shows a loading indicator while Pyodide downloads (~10MB WASM).
     * Falls back to JavaScript interpreter if Pyodide is unavailable.
     */
    async function init() {
        if (isReady) return;
        if (isLoading) {
            // Wait for existing load to finish
            return new Promise(resolve => onReadyCallbacks.push(resolve));
        }

        isLoading = true;

        // Try to load Pyodide first
        try {
            updateLoadingStatus('Loading Python runtime...', 'loading');

            // Check if loadPyodide is available
            if (typeof loadPyodide === 'undefined') {
                throw new Error('Pyodide not available');
            }

            // Load Pyodide
            pyodide = await loadPyodide({
                indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.27.4/full/'
            });

            updateLoadingStatus('Loading lipi-lang interpreter...', 'loading');

            // Fetch the lipi.py interpreter source
            lipiInterpreterSource = await fetchInterpreterSource();

            if (!lipiInterpreterSource) {
                throw new Error('Could not load lipi.py');
            }

            // Write lipi.py to the Pyodide virtual filesystem
            pyodide.FS.writeFile('/home/pyodide/lipi.py', lipiInterpreterSource);

            // Bootstrap: import the interpreter module so its functions are available
            await pyodide.runPythonAsync(`
import sys
sys.path.insert(0, '/home/pyodide')

# Import the lipi interpreter module
import importlib.util
spec = importlib.util.spec_from_file_location("lipi", "/home/pyodide/lipi.py")
lipi_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lipi_module)

# Make key functions available at global scope
from lipi import (
    eval_lipi_expr, run_lipi_line, execute_block,
    LipiRuntime, LipiReturnValue, LipiException,
    runtime as _runtime
)

def run_lipi_code(code):
    """
    Execute lipi-lang code and capture all output.
    Returns a dict with 'output' (captured stdout) and 'error' (if any).
    """
    import io
    import sys

    # Reset runtime state for each execution to avoid leaks between runs
    _runtime.functions = {}
    _runtime.python_modules = {}
    _runtime.modules = {}
    _runtime.exports = {}
    _runtime.loaded_modules = {}
    _runtime.module_stack = []
    _runtime.current_module_path = None
    _runtime.classes = {}

    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = captured = io.StringIO()

    error_msg = None
    try:
        env = {}
        lines = code.split('\\n')
        execute_block(lines, env)
    except LipiReturnValue:
        pass  # Top-level return is fine
    except LipiException as e:
        error_msg = str(e)
    except SyntaxError as e:
        error_msg = str(e)
    except Exception as e:
        error_msg = str(e)
    finally:
        sys.stdout = old_stdout

    output = captured.getvalue()
    return {'output': output, 'error': error_msg}
`);

            useFallbackInterpreter = false;
            isReady = true;
            isLoading = false;
            updateLoadingStatus('Python runtime ready', 'ready');

            console.log('✅ Lipi-lang running via Pyodide (Python)');

        } catch (err) {
            // Fall back to JavaScript interpreter
            console.warn('Pyodide unavailable, using native JavaScript interpreter:', err.message);
            
            useFallbackInterpreter = true;
            isReady = true;
            isLoading = false;
            updateLoadingStatus('JavaScript runtime ready', 'ready');

            console.log('✅ Lipi-lang running via JavaScript interpreter');
        }

        // Notify waiting callers
        onReadyCallbacks.forEach(cb => cb());
        onReadyCallbacks = [];
    }

    /**
     * Fetch the lipi.py interpreter source.
     * Tries relative path first (for local dev), then falls back to parent directory.
     */
    async function fetchInterpreterSource() {
        const paths = ['../src/lipi.py', './src/lipi.py', '/src/lipi.py'];

        for (const path of paths) {
            try {
                const resp = await fetch(path);
                if (resp.ok) {
                    return await resp.text();
                }
            } catch (_) {
                // Try next path
            }
        }

        // If fetch fails (e.g., file:// protocol), use the embedded interpreter
        return getEmbeddedInterpreterSource();
    }

    /**
     * Returns a minimal embedded version of the lipi interpreter
     * as a fallback when the full lipi.py cannot be fetched.
     * This covers the features used in the learning platform lessons.
     */
    function getEmbeddedInterpreterSource() {
        // This is a safety fallback - the real lipi.py should be served alongside
        // the learning platform. If we reach this, we'll use the JS interpreter.
        console.warn('Could not fetch lipi.py - will use native JavaScript interpreter');
        // Return null to signal we should use JS interpreter
        return null;
    }

    /**
     * Execute lipi-lang code through the real Python interpreter or JS fallback.
     * @param {string} code - lipi-lang source code
     * @returns {Promise<{output: string, error: string|null}>}
     */
    async function runCode(code) {
        if (!isReady) {
            await init();
        }

        // Use JavaScript fallback interpreter if Pyodide unavailable
        if (useFallbackInterpreter) {
            try {
                // Ensure the LipiInterpreter is loaded
                if (typeof LipiInterpreter === 'undefined') {
                    return { 
                        output: '', 
                        error: 'JavaScript interpreter not loaded. Please check that lipi-interpreter.js is included.' 
                    };
                }
                
                return LipiInterpreter.execute(code);
            } catch (err) {
                return { output: '', error: 'Execution error: ' + err.message };
            }
        }

        // Use Pyodide Python interpreter
        // Escape the code string for Python
        const escapedCode = code
            .replace(/\\/g, '\\\\')
            .replace(/"""/g, '\\"\\"\\"')
            .replace(/\n/g, '\\n');

        try {
            const result = await pyodide.runPythonAsync(`
import json
result = run_lipi_code("""${escapedCode}""")
json.dumps(result)
`);
            return JSON.parse(result);
        } catch (err) {
            return { output: '', error: 'Execution error: ' + err.message };
        }
    }

    /**
     * Update the loading status indicator in the UI.
     */
    function updateLoadingStatus(message, status) {
        const indicator = document.getElementById('pyodide-status');
        if (!indicator) return;

        indicator.textContent = message;
        indicator.className = 'pyodide-status pyodide-status-' + status;

        if (status === 'ready') {
            // Hide after a delay
            setTimeout(() => {
                indicator.classList.add('pyodide-status-hidden');
            }, 2000);
        }
    }

    /**
     * Check if the runtime is loaded and ready.
     */
    function ready() {
        return isReady;
    }

    return { init, runCode, ready };
})();
