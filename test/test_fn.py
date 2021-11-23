import unittest
from src.fn import handler
from aws_lambda_context import LambdaContext

class TestFn(unittest.TestCase):
    @classmethod
    def setupClass(cls):
        pass

    def test_handler(self):
        event = {
            "message": "hello world"
        }
        context = LambdaContext()
        context.aws_request_id = '92e5cc97-f8a2-46ac-a0cd-476c6084c42d'
        context.function_name = 'Fn'
        context.function_version = '$LATEST'
        context.invoked_function_arn = 'arn:aws:lambda:us-east-1:012345678912:function:Fn'
        context.memory_limit_in_mb = '128'
        context.log_group_name = 'aws/lambda/Fn'
        context.log_stream_name = '$LATEST'
        response = handler(event, context)
        self.assertEqual(event, response["body"]["event"])
        self.assertEqual(context.aws_request_id, response["body"]["aws_request_id"])
        self.assertEqual(context.function_name, response["body"]["function_name"])
        self.assertEqual(context.function_version, response["body"]["function_version"])
        self.assertEqual(context.invoked_function_arn, response["body"]["invoked_function_arn"])
        self.assertEqual(context.memory_limit_in_mb, response["body"]["memory_limit_in_mb"])
        self.assertEqual(context.log_group_name, response["body"]["log_group_name"])
        self.assertEqual(context.log_stream_name, response["body"]["log_stream_name"])

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestFn('test_handler'))
    runner = unittest.TextTestRunner(verbosity=0)
    runner.run(suite)
