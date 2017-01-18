import unittest
from tf import tf

VALID_CONFIG = {
  'project_root': '/tmp',
  'backend': {
    's3': {
      'config': {
        'bucket': 'tf-testing',
        'region': 'us-east-1'
      }
    }
  }
}

class ConigurationTest(unittest.TestCase):

  def test_env_stack_path(self):
    wrapper = tf.TF('test', 'qa', config=VALID_CONFIG)
    wrapper.build_path()
    self.assertEqual(wrapper.stack_path, "/tmp/stacks/test")

  def test_env_stack_state_file_path(self):
    wrapper = tf.TF('test', 'qa', config=VALID_CONFIG)
    wrapper.build_path()
    self.assertEqual(wrapper.tfstate_file_path, "/tmp/stacks/test/envs/qa.tfvars")

  def test_s3_backend_configuration_for_env_stack(self):
    wrapper = tf.TF('test', 'qa', config=VALID_CONFIG)
    wrapper.build_path()
    cmd = wrapper.get_s3_backend_config_command()
    self.assertSequenceEqual(cmd, [
      'terraform',
      'remote',
      'config',
      '-backend=s3',
      '-backend-config=bucket=tf-testing',
      '-backend-config=key=test/qa.tfstate',
      '-backend-config=region=us-east-1'
    ])
