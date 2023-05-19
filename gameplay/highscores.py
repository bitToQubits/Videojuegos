import pathlib
import traceback
import rendering.neon as neon

_BEST_SCORE = 0

 
def add_new_score(score, and_save=True):
    global _BEST_SCORE
    _BEST_SCORE = max(score, _BEST_SCORE)
    if and_save:
        save_score()


def get_best():
    return _BEST_SCORE


def save_score():
    path = get_path_to_score()
    try:
        ciphertext = _BEST_SCORE * neon.key
        if not path.exists():
            path.touch()
        with open(path, "w") as f:
            f.write("# no hacking allowed >:)\n{} \n".format(ciphertext))
    except Exception:
        print("ERROR: no se ha podido guardar.")
        traceback.print_exc()


def load_score():
    path = get_path_to_score()
    try:
        if path.exists():
            with open(path, "r") as f:
                lines = [line for line in f.readlines()]
                num = int(lines[1][:-2])
                if num % neon.key == 0:
                    global _BEST_SCORE
                    _BEST_SCORE = num // neon.key
                else:
                    print("WARN: puntaje alto no validado.")
    except Exception:
        print("ERROR: fallo para generar el mayor puntaje")
        traceback.print_exc()


def get_path_to_score():
    return pathlib.Path("highscore.txt")
