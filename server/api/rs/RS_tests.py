import RS 
import pytest


def show_vals(sad, joy, anger, calm):
    print("Sad: %d" %sad)
    print("Joy: %d" %joy)
    print("Anger: %d" %anger)
    print("Calm: %d" %calm)

# content of test_sample.py
def inc(x):
    return x + 1


def test_show_vals():
    assert RS.show_vals(5, 5, 5, 5) == 5