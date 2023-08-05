from ovos_local_backend.backend import start_backend
from ovos_config import Configuration


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--flask-port", help="Mock backend port number",
                        default=Configuration()["server"].get("port", 6712))
    parser.add_argument("--flask-host", help="Mock backend host",
                        default="127.0.0.1")
    args = parser.parse_args()
    start_backend(args.flask_port, args.flask_host)


if __name__ == "__main__":
    main()
