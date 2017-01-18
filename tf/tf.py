import argparse
import colors
import json
import os
import subprocess


GLOBAL_ENVIRONMENT_NAME='global'

class TF(object):
  '''
  Wrapper for configuration and running terraform commands
  '''

  def __init__(self, stack, environment, tfargs=[], config=None):
    self.stack = stack
    self.environment = environment
    self.tfargs = tfargs
    self.config = config

  def build_path(self):
    '''
    Setup the paths to where the stacks and the environments should be found
    '''
    stack_path = ''

    # If environment is not specified then we're targeting the global environment
    self.is_global_stack = (self.environment == GLOBAL_ENVIRONMENT_NAME)

    if(self.is_global_stack):
      self.stack_path = os.path.join(self.config['project_root'], 'global/{0}'.format(self.stack))
      self.tfstate_file_path = None
    else:
      self.stack_path = os.path.join(self.config['project_root'], 'stacks/{0}'.format(self.stack))
      self.tfstate_file_path = os.path.join(self.config['project_root'], 'stacks/{0}/envs/{1}.tfvars'.format(self.stack, self.environment))


  def validate_paths(self):
    '''
    Validate that we stacks and environments exist
    '''
    if (not self.config):
      colors.print_error('Could not find the .tfstate file')
      exit(1)

    if(not os.path.isdir(self.stack_path)):
      if(self.is_global_stack):
        colors.print_error('Could not find the global stack {0}'.format(self.stack))
      else:
        colors.print_error('Could not find the the {0} stack.'.format(self.stack, self.environment))
      exit(1)

    if((not self.is_global_stack) and (not os.path.isfile(self.tfstate_file_path))):
      colors.print_error('Could not find the {1} environment for the {0} stack.'.format(self.stack, self.environment))
      exit(1)


  def get_s3_backend_config_command(self):
    '''
    Returns the command to use for setting up s3 as the remote Terraform backend
    '''
    if (not 'backend' in self.config) or (not 's3' in self.config['backend']):
       colors.print_error('Missing s3 backend configuration.')
       exit(1)

    # Try deleting an existing state file
    try:
      os.remove(os.path.join(self.stack_path, ".terraform/terraform.tfstate"))
    except OSError as e:
      pass

    stack = 'global' if self.is_global_stack else self.stack
    env = self.stack if self.is_global_stack else self.environment

    command = self.get_tf_command('remote', [
      'config',
      '-backend=s3',
      '-backend-config=bucket={0}'.format(self.config['backend']['s3']['config']['bucket']),
      '-backend-config=key={0}/{1}.tfstate'.format(stack, env),
      '-backend-config=region={0}'.format(self.config['backend']['s3']['config']['region'])
    ], include_tfargs=False)

    env_vars = {}
    if ('profile' in self.config['backend']['s3']):
      env_vars['AWS_PROFILE'] = self.config['backend']['s3']['profile']

    return command, env_vars


  def get_tf_command(self, command, args=[], include_tfargs=True):
    '''
    Get the full terraform command to run
    '''

    # Certain commands need the environment state file to be passed in.
    if self.tfstate_file_path and (command in ['apply', 'destroy', 'plan', 'push', 'refresh']):
      args = args + ['-var-file={0}'.format(self.tfstate_file_path)]

    if include_tfargs:
      args = args + self.tfargs

    if not command in ['import', 'output', 'remote', 'taint', 'untaint' 'version']:
      args = args + [self.stack_path]

    return ['terraform', command] + args


  def execute_tf_command(self, command, include_tfargs=True):
    self.execute_command(self.get_tf_command(command, include_tfargs=include_tfargs))


  def execute_command(self, args, env_vars={}):
    '''
    Executes a subshell process
    '''
    colors.print_info("Command: {0}".format(' '.join(args)))

    # Get a copy of the current environment variables
    env = os.environ.copy()

    # Apply the top-level aws profile setting if it exists
    if ('aws' in self.config) and ('profile' in self.config['aws']):
      env['AWS_PROFILE'] = self.config['aws']['profile']

    # Combine the env_vars overrides with the current environment variabl
    env.update(env_vars)

    process = subprocess.Popen(args, cwd=self.stack_path, env=env)
    process.communicate()
    print("\n")

    if (process.returncode and process.returncode > 0):
      exit(process.returncode)


  def configure(self):
    '''
    Ensures the proper configuration is setup before executing Terraform commands
    '''
    command, env_vars = self.get_s3_backend_config_command()
    self.execute_command(command, env_vars)

