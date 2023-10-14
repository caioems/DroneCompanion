import os,subprocess

# Run cProfile on your Python application
cprofiler_command = "python -m cProfile -o run.prof run.py"
subprocess.call(cprofiler_command, shell=True)

# Run SnakeViz to visualize the profile data
with "run.prof" as file:
    snakeviz_command = f"snakeviz {file}"
    subprocess.call(snakeviz_command, shell=True)
os.remove(file)