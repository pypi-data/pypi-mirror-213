import asyncio

from metalayer.chatgpt import complete, complete_async
from metalayer.chatgpt.utils import load_prompts, fill_messages, retry_on_exception


system_prompt, user_prompt = load_prompts('activity_log')

completion_params = {
    'temperature': 0
}

def log_activity(text):
    messages = fill_messages(system_prompt, user_prompt, text)
    raw_output = complete(messages, **completion_params)
    summary, activity, info, *_ = raw_output.split('\n\n')

    summary = summary.split(':')[-1].strip()
    activity = activity.split(':')[-1].strip()
    info = info.split(':')[-1].strip().split('\n')
    info = [i.strip(' -') for i in info]

    return {
        'summary': summary,
        'activity': activity,
        'info': info
    }


@retry_on_exception(retries=5, initial_wait_time=1)
async def log_activity_async(text):
    messages = fill_messages(system_prompt, user_prompt, text)
    raw_output = await complete_async(messages, **completion_params)
    summary, activity, info, *_ = raw_output.split('\n\n')

    summary = summary.split(':')[-1].strip()
    activity = activity.split(':')[-1].strip()
    info = info.split(':')[-1].strip().split('\n')
    info = [i.strip(' -') for i in info]

    return {
        'summary': summary,
        'activity': activity,
        'info': info
    }

if __name__ == '__main__':
    s = """CGWindowListCre X
E What does the me X
Backend Researci X
Research D
X
Backend Research X 3 openai/openai-pyl X
Kalman-and-Baye X
executeAndReturr X g New Tab
RE Handling the keyb
github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python/blob/master/04-One-Dimensional-Kalman-Filters.ipynt
L
A Drive
Gmail 14| Calendar
D YouTube (39 Discord 7 Crowdmark L Learn @WaterlooWorks E New Doc | New Sheet
M MEGA
Q Search or jump
Pull requests Issues Codespaces Marketplace Explore
4
. rabe / Kalman-and-Bayesian-Filters-in-Python(Public
O Watch 461
89 Fork 3.7k
4 Star 13.7k
(› Code
© Issues 87 13 Pull requests 10
O Actions B Projects N Wiki ® Security L~ Insights
MI
- master
Kalman-and-Bayesian-Filters-in-Python/04-One-Dimensional-Kalman-Filters.ipynb9
Q Go to file
rlabbe switch to f-strings -
cd962f3 last ye:
© History
Preview Code Blame
4013 lines (4013 loc) • 1.36 MB
Raw ru
Table of Contents
One Dimensional Kalman Filters
In [1]:
@matplotlib inline
In [2]:
#format the book
import
format
book format set style()
Out (2]:
Now that we understand the discrete Bayes filter and Gaussians
are prepared to implement a Kalman filter. We will do this exactly
as we did the discrete Bayes filter rather than starting with equations we will develop the code step by step based on reasoning
about the problem.
"One dimensional" means that the filter only tracks one state variable, such as position on the x-axis. In subsequent chapters we will
learn a more general multidimensional form of the filter that can track many state variables simultaneously, such as position, velocity,
and acceleration. Recall that we used velocity in the g-h filter to get better estimates t
by tracking position alone. The same is true
for the Kalman filter.
So why not just jump into the multidimensional form of the filter? To be honest, the math is difficult, and my intuitive approach to
developing the filter starts to break down. O This math obscures the rather simple principles that allow the Kalman filter to work.
So, in this chapter we learn how to use Gaussians to implement a Bayesian filter. That's all the Kalman filter is - a Bayesian filter that
Gaussians. In the
chaptel
will switch 1 a multidimensional form : the
power of the Kalman filter will
unleashed!
Problem Description"""

    async def test():
        loop = asyncio.get_event_loop()
        tasks = []
        for _ in range(10):
            tasks.append(loop.create_task(log_activity_async(s)))
        await asyncio.gather(*tasks)

    asyncio.run(log_activity_async(s))
    print('Done!')
