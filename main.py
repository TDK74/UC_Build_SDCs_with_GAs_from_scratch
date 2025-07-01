import subprocess
import sys


def main():
    """
    Runs the training pipeline for self-driving cars across tracks 0 to 3,
    each with 34 agents over 5 rounds. Then performs a test drive with
    the top 4 agents on an unseen track (track 4) over 4 evaluation rounds.
    """

    print("\n>>> LAUNCHING TRAINING PIPELINE <<<\n")
    subprocess.run([sys.executable, "training.py"], check=True)

    print("\n>>> LAUNCHING TESTDRIVE <<<\n")
    subprocess.run([sys.executable, "testdrive.py"], check=True)

    print("\n>>> ALL DONE — THE CYCLE TRAINING - TESTING IS COMPLETE! <<<")


if __name__ == "__main__":
    main()
