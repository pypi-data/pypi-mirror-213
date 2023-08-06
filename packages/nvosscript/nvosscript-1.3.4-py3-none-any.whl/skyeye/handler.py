from skyeye import remote,loghandler
from start import login



def command_env(env=None):
    if env is None:
        result = remote.get_current_env()
        print(f"current env:{result['env']} this cloud linked:{result['tip']}")
        return
    remote.switch_env(env)


def command_log(path):
    status = login.check_login_status()
    if not status:
        print("Please login first. you could use login command to login this script")
        return
    loghandler.filter_effective_log(path)
