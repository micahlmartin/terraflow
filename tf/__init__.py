import colors
import json
import os
import tf
from args import parse_args


def find_project_root(path=None):
  path = path if path else os.getcwd()

  if os.path.isfile(os.path.join(path, '.tfconfig')):
    return path
  else:
    new_path = os.path.dirname(path)
    if new_path == path:
      return None

    return find_project_root(os.path.dirname(path))


def load_config():
  project_root = find_project_root()

  if not project_root:
    return None

  config = None

  with open(os.path.join(project_root, '.tfconfig')) as config_file:
    try:
      config = json.load(config_file)
      config['project_root'] = project_root
    except ValueError as e:
      # print(e)
      pass

  return config


def main():

  args = parse_args()

  wrapper = tf.TF(
    args.stack,
    args.environment,
    tfargs=args.tfargs,
    config=load_config()
  )

  wrapper.build_path()
  wrapper.validate_paths()

  colors.print_heading('========> Configuring state backend')
  wrapper.configure()

  # Always make sure we have the modules
  colors.print_heading('========> Updating the modules')
  wrapper.execute_tf_command('get', include_tfargs=False)

  colors.print_heading("========> Exucuting terraform {0}".format(args.command))
  wrapper.execute_tf_command(args.command)
