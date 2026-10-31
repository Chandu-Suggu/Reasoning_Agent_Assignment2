import json
import sys
import io
import contextlib

def run_notebook(nb_path):
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    global_scope = {"__name__": "__main__"}
    
    print(f"Executing cells in {nb_path}...")
    for idx, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code':
            code = "".join(cell['source'])
            stdout_capture = io.StringIO()
            stderr_capture = io.StringIO()
            
            print(f"  Running cell {idx + 1}...")
            try:
                with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
                    exec(code, global_scope)
                
                out_text = stdout_capture.getvalue()
                err_text = stderr_capture.getvalue()
                
                outputs = []
                if out_text:
                    outputs.append({
                        "name": "stdout",
                        "output_type": "stream",
                        "text": out_text.splitlines(keepends=True)
                    })
                if err_text:
                    outputs.append({
                        "name": "stderr",
                        "output_type": "stream",
                        "text": err_text.splitlines(keepends=True)
                    })
                cell['outputs'] = outputs
                cell['execution_count'] = idx + 1
            except Exception as e:
                print(f"Error in cell {idx + 1}: {e}")
                cell['outputs'] = [{
                    "ename": type(e).__name__,
                    "evalue": str(e),
                    "output_type": "error",
                    "traceback": [f"{type(e).__name__}: {str(e)}"]
                }]
                raise

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=2)
    print(f"Successfully executed and updated {nb_path} with all cell outputs!")

if __name__ == '__main__':
    run_notebook('submission/reasoning_agent.ipynb')
