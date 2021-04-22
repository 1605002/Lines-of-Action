mkfifo pipe
g++ AI.cpp -o one
python3 game.py < pipe | ./one > pipe
rm one
rm pipe
# python3 two.py < pipe | ./one > pipe  # using this instead will not show output in the terminal