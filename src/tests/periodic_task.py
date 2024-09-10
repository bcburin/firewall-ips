from time import sleep

from src.services.task import PeriodicTask


if __name__ == '__main__':
    # create tasks
    def hw_and_wait(n: int):
        def inner():
            print(f"[{n}] Hello, World!")
            sleep(5)
            print(f"[{n}] Finished waiting process")
        return inner
    hw0 = PeriodicTask(cron_string="* * * * *", task=hw_and_wait(0), run_on_start=True)
    hw1 = PeriodicTask(cron_string="* * * * *", task=hw_and_wait(1), run_on_start=False)
    hw2 = PeriodicTask(cron_string="* * * * *", task=hw_and_wait(2), run_on_start=True)
    hw3 = PeriodicTask(cron_string="* * * * *", task=hw_and_wait(3), run_on_start=False)
    # run tasks
    hw0.run()
    hw1.run()
    hw2.run()
    hw3.run()
