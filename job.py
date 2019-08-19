import sys, os
#insert file into path for code capture
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, root_dir)
import backtracepython as bt

host, port = sys.argv[1:]

bt.initialize(
    endpoint="https://submit.backtrace.io/testing-xebialabs/e958cfd2940e7bdb2d60fdf7fd22d4caaecdb9966efc835e24054a247aef6162/json",
    token="e958cfd2940e7bdb2d60fdf7fd22d4caaecdb9966efc835e24054a247aef6162",
    context_line_count=2
)

example_local_var = "hello this is my value"

a = b
