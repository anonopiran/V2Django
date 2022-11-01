import shlex
import subprocess

from django.utils import autoreload


class BaseCommand:
    _cmd_run = None

    def add_arguments(self, parser):
        parser.add_argument(
            "--auto-reload", action="store_true", help="enable auto reload"
        )
        parser.add_argument(
            "celery-args",
            nargs="*",
            help="args passed to celery",
            default=False,
        )

    def handle(self, *_, **options):
        _args = options["celery-args"]
        _args = " ".join(_args) if _args else ""
        if options["auto_reload"]:
            print("Starting celery worker with autoreload...")
            autoreload.run_with_reloader(self._restart_celery, args=_args)
        else:
            print("Starting celery worker...")
            self._run(args=_args)

    def _restart_celery(self, args: str):
        cmd_kill = f'pkill -f "{self._cmd_run}"'
        subprocess.call(shlex.split(cmd_kill))
        self._run(args)

    def _run(self, args: str):
        cmd = f"{self._cmd_run} {args}"
        print(f"running {cmd}")
        subprocess.call(shlex.split(cmd))
