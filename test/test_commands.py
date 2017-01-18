import unittest
from tf import tf

VALID_CONFIG = {
  'project_root': '/tmp'
}

class CommandsTest(unittest.TestCase):

  def test_terraform_command_with_arguments(self):
    wrapper = tf.TF('test', 'qa', tfargs=['-target', 'test', '-Xdestroy', '-target=./mymodule'], config=VALID_CONFIG)
    wrapper.build_path()
    cmd = wrapper.get_tf_command('plan')

    self.assertSequenceEqual(cmd, [
      'terraform',
      'plan',
      '-var-file={0}'.format(wrapper.tfstate_file_path),
      '-target',
      'test',
      '-Xdestroy',
      '-target=./mymodule',
      wrapper.stack_path
    ])

  def test_terraform_command_without_arguments(self):
    wrapper = tf.TF('test', 'plan', tfargs=[], config=VALID_CONFIG)
    wrapper.build_path()
    cmd = wrapper.get_tf_command('plan')

    self.assertSequenceEqual(cmd, [
      'terraform',
      'plan',
      '-var-file={0}'.format(wrapper.tfstate_file_path),
      wrapper.stack_path
    ])
