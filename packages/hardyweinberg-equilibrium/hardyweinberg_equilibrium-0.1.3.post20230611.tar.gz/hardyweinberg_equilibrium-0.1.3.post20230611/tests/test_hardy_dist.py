import sys
import subprocess


def test_hardy_dist():
    # implement pip as a subprocess:
    print(sys.executable)
    # subprocess.check_call([sys.executable, '-m', 'pip', 'install',
    #                        '../hardy_weinberg_equilibrium-0.1.0.post20230610-py3-none-any.whl'])
    # sys.argv = [sys.argv[0], "--verbose", "--ppop", "639", "--qpop", "392", "--pq2pop", "1003"]
