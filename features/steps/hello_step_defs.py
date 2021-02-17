from behave import *
from cli_project.hello import parse_args

@given('we run the hello command with name argument')
def step_impl(context):
    context.cli = parse_args(['hello', '--name', 'dimitri'])

@then('the command returns "hello dimitri"')
def step_impl(context):
    args = context.cli
    assert args.hello == 'hello'
    assert args.name == 'dimitri'
