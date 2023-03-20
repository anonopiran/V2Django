from django.core.management.base import BaseCommand, CommandParser
import shlex
import subprocess

from django.utils import autoreload


class Command(BaseCommand):
    requires_system_checks = []
    help = "Start a celery worker"
    _cmd_run = "celery -A V2Django worker --statedb=./storage/worker.state"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            "--auto-reload", action="store_true", help="enable auto reload"
        )
        parser.add_argument(
            "--due-date-q",
            action="store_true",
            help="subscribe to due date queue",
        )
        parser.add_argument(
            "--f2u-q",
            action="store_true",
            help="subscribe to fly2users client queue",
        )
        parser.add_argument(
            "celery-args",
            nargs="*",
            action="append",
            help="extra args passed to celery",
            default=[],
        )

    @staticmethod
    def arg_gen(options):
        ddq = options["due_date_q"]
        f2uq = options["f2u_q"]
        assert (
            ddq or f2uq
        ), "at least one of --due-date-q or --f2u-q should be specified"
        _args = options["celery-args"][0]
        q_ = [
            val
            for cond, val in ((ddq, "long_duedate_tasks"), (f2uq, "f2u_tasks"))
            if cond
        ]
        _args.append(f"-Q {','.join(q_)}")
        _args = " ".join(_args)
        return _args

    def handle(self, *_, **options):
        _args = self.arg_gen(options)
        if options["auto_reload"]:
            print("Starting celery worker with autoreload...")
            autoreload.run_with_reloader(self._restart_celery, args=_args)
        else:
            self._run(args=_args)

    def _restart_celery(self, args: str):
        cmd_kill = f'pkill -f "{self._cmd_run}"'
        subprocess.call(shlex.split(cmd_kill))
        self._run(args)

    def _run(self, args: str):
        cmd = f"{self._cmd_run} {args}"
        print(f"running {cmd}")
        subprocess.call(shlex.split(cmd))
