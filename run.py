import subprocess
import sys


def main():
    print("Starting Elyx Healthcare Journey Simulation UI...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "ui/streamlit_app.py"])  # noqa: S603


if __name__ == "__main__":
    main()

