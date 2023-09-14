import os


def ignore_stdout(func):
    """
    Wrapper function to not print out stdout and stderr for the function
    that gets passed here.
    Usage example:
    ```
    @ignore_stdout
    def my_function(var):
        return var
    ```
    """

    def wrapper(*args, **kwargs):
        # Backup the original file descriptors for stdout and stderr
        original_stdout_fd = os.dup(1)
        original_stderr_fd = os.dup(2)

        # Open a null file for writing
        devnull = os.open(os.devnull, os.O_WRONLY)

        # Duplicate the null file descriptors onto stdout and stderr
        os.dup2(devnull, 1)
        os.dup2(devnull, 2)
        try:
            return func(*args, **kwargs)
        finally:
            # Restore the original file descriptors
            os.dup2(original_stdout_fd, 1)
            os.dup2(original_stderr_fd, 2)

            # Close the backups and the null file
            os.close(original_stdout_fd)
            os.close(original_stderr_fd)
            os.close(devnull)

    return wrapper
