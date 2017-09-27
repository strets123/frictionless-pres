from datapackage_pipelines.wrapper import ingest, spew
import logging
import subprocess


def log_subprocess_output(pipe):
    for line in iter(pipe.readline, b''): # b'\n'-separated lines
        logging.info('got line from subprocess: %r', line)


def run_shell_command(command_line_args):

    logging.info('Subprocess: "' + ' '.join(command_line_args) + '"')

    try:
        command_line_process = subprocess.Popen(
            command_line_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        with command_line_process.stdout:
            log_subprocess_output(command_line_process.stdout)
    except (OSError, subprocess.CalledProcessError) as exception:
        logging.info('Exception occured: ' + str(exception))
        logging.info('Subprocess failed')
        raise exception
    else:
        # no exception was raised
        logging.info('Subprocess finished')

    return True


parameters, datapackage, res_iter = ingest()

run_shell_command(
    parameters["arguments"]
)

spew(datapackage, res_iter)
