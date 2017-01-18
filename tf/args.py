import argparse

def parse_args():
  parser = argparse.ArgumentParser("tf")

  parser.add_argument('command', help="Terraform command to execute")
  parser.add_argument('stack', help="The name of the stack to target.")
  parser.add_argument('environment', help="The name of the environment to target. If not specified then it is assumed to be targeting a global stack.")
  # parser.add_argument('--profile', '-p', help="The AWS profile to lookup credentials for.")
  parser.add_argument('tfargs', nargs=argparse.REMAINDER, help='Additional arguments to passthrough to Terraform.')

  return parser.parse_args()
