from ..ext.hist import hist_tail
import os

def run_command(n_lines: list):
    # TODO: what if non-default n lines has been pased to hist
    df = hist_tail(20)
    exec_line = ''
    for cmd in n_lines:
        exec_line += f"{df.iloc[cmd].Command}"
        exec_line += ' && '

    print(f"Running {exec_line[:-4]}")
    os.system(exec_line[:-4])
    # print(exec_line[:-4])