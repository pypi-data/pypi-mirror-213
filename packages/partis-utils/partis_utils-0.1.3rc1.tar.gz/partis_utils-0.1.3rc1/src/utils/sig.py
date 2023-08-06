import signal
import time
import sys

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
listenable = [
  sig
  for sig in signal.Signals
  if sig not in [ signal.SIGKILL, signal.SIGSTOP ] ]

listeners = {
  sig : list()
  for sig in listenable }

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def install_signal_hook(sig):
  if sig not in listenable:
    raise ValueError(f"Cannot handle signal: {sig.name}")

  prev_handler = None

  def sig_handler(_sig, frame):

    for f in listeners[sig]:
      try:
        f(sig)
      except:
        pass

    if callable(prev_handler):
      prev_handler(_sig, frame)

  prev_handler = signal.signal(sig, sig_handler)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
for sig in listenable:
  install_signal_hook(sig)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def add_signal_listener(sig, f):
  if sig not in listenable:
    raise ValueError(f"Cannot listen for signal: {sig.name}")

  l = listeners[sig]

  if f not in l:
    l.append(f)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def remove_signal_listener(sig, f):
  l = listeners[sig]

  if f in l:
    l.remove(f)
