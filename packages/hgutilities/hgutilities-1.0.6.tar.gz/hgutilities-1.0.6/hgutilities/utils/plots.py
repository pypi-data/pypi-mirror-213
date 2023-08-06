import matplotlib.pyplot as plt

def maximise_figure():
    mng = plt.get_current_fig_manager()
    maximise_figure_attempt_1(mng)

def maximise_figure_attempt_1(mng):
    try:
        mng.resize(*mng.window.maxsize())
    except:
        maximise_figure_attempt_2(mng)

def maximise_figure_attempt_2(mng):
    try:
        mng.window.fullscreen()
    except:
        maximise_figure_attempt_3(mng)

def maximise_figure_attempt_3(mng):
    try:
        mng.window.state('zoomed')
    except:
        maximise_figure_attempt_4(mng)

def maximise_figure_attempt_4(mng):
    try:
        full_screen_toggle()
    except:
        print("Could not maximise figure window")
