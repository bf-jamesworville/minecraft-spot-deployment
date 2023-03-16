- Add ECS Exec: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-exec.html
- Capture an interruption - send a notification
- Disable ECS capacity provider from terminating / provisioning instances due to ECS task requirements
- Check task count
- Fix handler for /status when off and wait time when off
- If there is a reason it can't scale up or down, then return the reason
- Throw exceptions to the client
- Handle scaling activity in progress
- CloudFront -> R53
- Alerts on scale down
- Amend CPU credits
- Check if the desired capacity is 1 but actual status
- Move domain back?

Handle exceptions like this:
```python
class MyClass:
    def handle_exceptions(self, func):
        try:
            func()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def my_method(self):
        self.handle_exceptions(lambda: some_code_that_might_raise_an_exception())
        self.handle_exceptions(lambda: some_other_code_that_might_raise_an_exception())
        return "Success"

```